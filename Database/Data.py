from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger

from sqlalchemy import delete, select, update
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

from Database.Models import *
from Database.Schedule import *
from Utils.Logger import Logger
from Settings.Config import DATABASE_URL


class Database:

    def __init__(self):

        # Session
        self.engine = create_async_engine(url=DATABASE_URL, echo=True)
        self.async_session = async_sessionmaker(self.engine, expire_on_commit=False)

        # Logger
        self.logger = Logger()

        # Schedule
        self.scheduler = AsyncIOScheduler()
        self.scheduler.add_job(
            ...,
            trigger=CronTrigger(day_of_week="mon", hour="3", minute="33")
        )

    # --> INIT METHOD

    async def init_all(self):
        try:
            async with self.engine.begin() as connection:
                await connection.run_sync(Base.metadata.create_all)

            async with self.async_session as session:
                d_exists = (await session.execute(select(Day).limit(1)).scalar())
                s_exists = (await session.execute(select(Subject).limit(1)).scalar())
                hw1_exists = (await session.execute(select(HomeworkWeek1).limit(1)).scalar())
                hw2_exists = (await session.execute(select(HomeworkWeek2).limit(1)).scalar())

                # Day Init
                if not d_exists:
                    session.add_all([Day(day=day) for day in days])
                    await session.commit()

                # Subject Init
                if not s_exists:
                    session.add_all([Subject(subject=subject) for subject in subjects])
                    await session.commit()

                # HomeworkWeek1 Init
                if not hw1_exists:
                    hw1_data = [
                        HomeworkWeek1(
                            day_id=_[0],
                            subject_id=_[1],
                            assignment=" - ",
                            image=" - "
                        ) for _ in schedule
                    ]
                    session.add_all(hw1_data)
                    await session.commit()

                # HomeworkWeek2 Init
                if not hw2_exists:
                    hw2_data = [
                        HomeworkWeek2(
                            day_id=_[0],
                            subject_id=_[1],
                            assignment=" - ",
                            image=" - "
                        ) for _ in schedule
                    ]
                    session.add_all(hw2_data)
                    await session.commit()

                self.logger.log_info("[INFO] -> Database successfully initialized")
        except SQLAlchemyError as exception:
            self.logger.log_error(f"[FAIL] -> while initializing database : {exception}")

    # --> USER METHODS

    async def create_user(
            self,
            telegram_id: int,
            username: str
    ):
        try:
            async with self.async_session() as session:
                query = (await session.execute(select(User).where(User.telegram_id == telegram_id))).scalar()

                if not query:
                    session.add(User(telegram_id=telegram_id, username=username))
                    await session.commit()

        except SQLAlchemyError as exception:
            self.logger.log_error(f"[FAIL] -> while creating user: {exception}")

    async def update_user(
            self,
            telegram_id: int,
            field: str,
            value: str
    ):
        try:
            async with self.async_session() as session:
                query = (await session.execute(select(User).where(User.telegram_id == telegram_id))).scalar()

                if query:
                    await session.execute(
                        update(User).where(User.telegram_id == telegram_id).values({field: value})
                    )
                    await session.commit()

        except SQLAlchemyError as exception:
            self.logger.log_error(f"[FAIL] -> while updating user : {exception}")

    async def get_user(
            self,
            telegram_id: int,
            field: str,
    ):
        try:
            async with self.async_session() as session:
                query = (await session.execute(select(User).where(User.telegram_id == telegram_id))).scalar()

                if query:
                    await session.execute(
                        select(getattr(User, field)).where(User.telegram_id == telegram_id).limit(1)
                    )
                    await session.commit()

        except SQLAlchemyError as exception:
            self.logger.log_error(f"[FAIL] -> while getting user : {exception}")

    # --> SCHEDULED METHOD

    async def scheduled(self):
        try:
            async with self.async_session() as session:

                # Update HomeworkWeek1

                await session.execute(delete(HomeworkWeek1))

                query = (await session.execute(select(HomeworkWeek2))).scalars().all()

                entry = [
                    HomeworkWeek1(
                        day_id=entry.day_id,
                        subject_id=entry.subject_id,
                        assignment=entry.assignment,
                        image=entry.image
                    )
                    for entry in query
                ]
                session.add_all(entry)

                # Clean HomeworkWeek2

                await session.execute(delete(HomeworkWeek2))

                entry = [
                    HomeworkWeek2(
                        day_id=entry[0],
                        subject_id=entry[1],
                        subgroup_id=entry[2],
                        homework=' - ',
                        image=' - '
                    )
                    for entry in schedule
                ]
                session.add_all(entry)

        except SQLAlchemyError as exception:
            self.logger.log_error(f"[FAIL] -> while migrating data from 'week 2' to 'week 1' : {exception}")

    # --> HOMEWORK METHODS

    async def add_homework(
            self,
            week_id: int,
            day_id: int,
            subject_id: int,
            assignment: str,
            image: str | None
    ):
        try:
            async with self.async_session() as session:
                week = HomeworkWeek1 if week_id == 1 else HomeworkWeek2

                query = week(day_id=day_id, subject_id=subject_id, assignment=assignment, image=image)
                session.add(query)

        except SQLAlchemyError as exception:
            self.logger.log_error(f"[FAIL] -> while adding homework : {exception}")

    async def get_homework(self) -> list:
        try:
            async with self.async_session as session:
                query = await session.execute(
                    select(
                        Day.day,
                        Subject.subject,
                        HomeworkWeek1.assignment,
                        HomeworkWeek1.image,
                    )
                    .union_all(
                        select(
                            Day.day,
                            Subject.subject,
                            HomeworkWeek2.assignment,
                            HomeworkWeek2.image,
                        )
                        .join(Day, HomeworkWeek2.day_id == Day.id)
                        .join(Subject, HomeworkWeek2.subject_id == Subject.id)
                    ))

                data = [
                    {
                        "day": day,
                        "subject": subject,
                        "assignment": assignment or "No Assignment",
                        "image": image or "No Image"
                    } for day, subject, assignment, image in query.all()
                ]

                return data

        except SQLAlchemyError as exception:
            self.logger.log_error(f"[FAIL] -> while getting homework : {exception}")
