from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger

from sqlalchemy import delete, select, update
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

from Database.Models import *
from Database.Schedule import *
from Utils.Logger import logger
from Settings.Config import DATABASE_URL


class Database:

    def __init__(self):

        # Session
        self.engine = create_async_engine(url=DATABASE_URL, echo=True)
        self.async_session = async_sessionmaker(self.engine, expire_on_commit=False)

        # Schedule
        self.scheduler = AsyncIOScheduler()
        self.scheduler.add_job(
            self.scheduled,
            trigger=CronTrigger(day_of_week="mon", hour="3", minute="33")
        )

    # --> INIT METHODS

    async def init_all(self):
        try:
            async with self.engine.begin() as connection:
                await connection.run_sync(Base.metadata.create_all)

                await self.init_days()
                await self.init_subjects()
                await self.init_homework()

            logger.log_info("[INFO] -> Successfully created tables")
        except SQLAlchemyError as exception:
            logger.log_error(f"[FAIL] -> while creating tables : {exception}")

    async def init_days(self):
        try:
            async with self.async_session() as session:
                days_exists = await session.execute(select(Day))

                if not days_exists.first():
                    session.add_all([Day(day=day) for day in days])
                    await session.commit()

            logger.log_info("[INFO] -> Successfully initialized days")
        except SQLAlchemyError as exception:
            logger.log_error(f"[FAIL] -> while initializing days : {exception}")

    async def init_subjects(self):
        try:
            async with self.async_session() as session:
                subjects_exists = await session.execute(select(Subject))

                if not subjects_exists.first():
                    session.add_all([Subject(subject=subject) for subject in subjects])
                    await session.commit()

            logger.log_info("[INFO] -> Successfully initialized subjects")
        except SQLAlchemyError as exception:
            logger.log_error(f"[FAIL] -> while initializing subjects : {exception}")

    async def init_homework(self):
        try:
            async with self.async_session() as session:
                homeworkweek1_exists = await session.execute(select(HomeworkWeek1))
                homeworkweek2_exists = await session.execute(select(HomeworkWeek2))

                if not homeworkweek1_exists.first():
                    homeworkweek1_data = [
                        HomeworkWeek1(
                            day_id=_[0],
                            subject_id=_[1],
                            assignment="No assignment",
                            image="No images"
                        ) for _ in schedule
                    ]
                    session.add_all(homeworkweek1_data)
                    await session.commit()

                if not homeworkweek2_exists.first():
                    homeworkweek2_data = [
                        HomeworkWeek2(
                            day_id=_[0],
                            subject_id=_[1],
                            assignment="No assignment",
                            image="No images"
                        ) for _ in schedule
                    ]
                    session.add_all(homeworkweek2_data)
                    await session.commit()

            logger.log_info("[INFO] -> Successfully initialized homework tables")
        except SQLAlchemyError as exception:
            logger.log_error(f"[FAIL] -> while initializing homework : {exception}")

    # --> USER METHODS

    async def add_user(
            self,
            telegram_id: int,
            username: str
    ):
        try:
            async with self.async_session() as session:
                query = await session.execute(
                    select(User).
                    where(User.telegram_id == telegram_id)
                )

                if not query.scalar():
                    session.add(User(telegram_id=telegram_id, username=username))
                    await session.commit()

        except SQLAlchemyError as exception:
            logger.log_error(f"[FAIL] -> while creating user: {exception}")

    async def update_user(
            self,
            telegram_id: int,
            field: str,
            value: str
    ):
        try:
            async with self.async_session() as session:
                query = await session.execute(
                    select(User).
                    where(User.telegram_id == telegram_id)
                )

                if query.scalar():
                    await session.execute(
                        update(User).
                        where(User.telegram_id == telegram_id).
                        values({field: value})
                    )
                    await session.commit()

        except SQLAlchemyError as exception:
            logger.log_error(f"[FAIL] -> while updating user : {exception}")

    async def get_user(
            self,
            telegram_id: int,
            field: str,
    ):
        try:
            async with self.async_session() as session:
                query = await session.execute(
                    select(getattr(User, field)).where(User.telegram_id == telegram_id).limit(1)
                )

                query = query.scalars().first()
                if query is not None:
                    return query

        #         TODO: FIX BUG


        except SQLAlchemyError as exception:
            logger.log_error(f"[FAIL] -> while getting user : {exception}")

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
            logger.log_error(f"[FAIL] -> while adding homework : {exception}")

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
                        "assignment": assignment,
                        "image": image
                    } for day, subject, assignment, image in query.all()
                ]

                return data

        except SQLAlchemyError as exception:
            logger.log_error(f"[FAIL] -> while getting homework : {exception}")

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
            logger.log_error(f"[FAIL] -> while migrating data from 'week 2' to 'week 1' : {exception}")


database = Database()
