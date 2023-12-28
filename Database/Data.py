from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger

from sqlalchemy import delete, select, update, and_
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

from Database.Models import *
from Database.Schedule import *
from Utils.Logger import logger
from Settings.Config import DATABASE_URL, CRON_TRIGGER_DAY_OF_WEEK, CRON_TRIGGER_HOUR, CRON_TRIGGER_MINUTE


class Database:

    def __init__(self):

        # Session
        self.engine = create_async_engine(url=DATABASE_URL, echo=False)
        self.async_session = async_sessionmaker(self.engine, expire_on_commit=False)

        # Schedule
        self.scheduler = AsyncIOScheduler()
        self.scheduler.add_job(
            self.scheduled,
            trigger=CronTrigger(
                day_of_week=CRON_TRIGGER_DAY_OF_WEEK,
                hour=CRON_TRIGGER_HOUR,
                minute=CRON_TRIGGER_MINUTE)
        )

    # --> INIT METHODS

    async def init_all(self):
        try:
            await self.init_metadata()
            await self.init_days()
            await self.init_subjects()
            await self.init_homework()

            logger.log_info(f"{f'Database initialization successfully completed'.ljust(46)} ::")
        except SQLAlchemyError as exception:
            logger.log_error(f"{f'Database initialization failed'.ljust(46)} :: {exception}")

    async def init_metadata(self):
        try:
            async with self.engine.begin() as connection:
                await connection.run_sync(Base.metadata.create_all)

            logger.log_info(f"{'Metadata initialization completed'.ljust(46)} ::")
        except SQLAlchemyError as exception:
            logger.log_error(f"{'Metadata initialization failed'.ljust(46)} :: {exception}")

    async def init_days(self):
        try:
            async with self.async_session() as session:
                days_exists = await session.execute(select(Day))

                if not days_exists.first():
                    session.add_all([Day(day=day) for day in days])
                    await session.commit()

            logger.log_info(f"{f'DayTable successfully initialized'.ljust(46)} ::")

        except SQLAlchemyError as exception:
            logger.log_error(f"{f'DayTable initialization failed'.ljust(46)} :: {exception}")

    async def init_subjects(self):
        try:
            async with self.async_session() as session:
                subjects_exists = await session.execute(select(Subject))

                if not subjects_exists.first():
                    session.add_all([Subject(subject=subject) for subject in subjects])
                    await session.commit()

            logger.log_info(f"{f'SubjectTable successfully initialized'.ljust(46)} ::")

        except SQLAlchemyError as exception:
            logger.log_error(f"{f'SubjectTable initialization failed'.ljust(46)} :: {exception}")

    async def init_homework(self):
        try:
            async with self.async_session() as session:
                homeworkweek1_exists = await session.execute(select(HomeworkWeek1))
                homeworkweek2_exists = await session.execute(select(HomeworkWeek2))

                if not homeworkweek1_exists.first():
                    homeworkweek1_data = [
                        HomeworkWeek1(
                            week_id=1,
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
                            week_id=2,
                            day_id=_[0],
                            subject_id=_[1],
                            assignment="No assignment",
                            image="No images"
                        ) for _ in schedule
                    ]
                    session.add_all(homeworkweek2_data)
                    await session.commit()

            logger.log_info(f"{f'HomeworkWeekTable successfully initialized'.ljust(46)} ::")

        except SQLAlchemyError as exception:
            logger.log_error(f"{f'HomeworkWeekTable initialization failed'.ljust(46)} :: {exception}")

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
            logger.log_error(f"{f'Failed to add user {telegram_id}'.ljust(46)} :: {exception}")

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
            logger.log_error(f"{f'Failed to update user {telegram_id}'.ljust(46)} :: {exception}")

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

                if query:
                    return query

        except SQLAlchemyError as exception:
            logger.log_error(f"{f'Failed to retrieve user {telegram_id}'.ljust(46)} :: {exception}")

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
                await session.commit()

            logger.log_info(f"{f'Homework added successfully ({week_id}{day_id}.{subject_id})'.ljust(46)} ::")
        except SQLAlchemyError as exception:
            logger.log_error(f"{f'Failed to add homework '.ljust(46)} :: {exception}")

    async def get_homework(
            self,
            week_id: int,
            day_id: int
    ) -> list:
        try:
            async with self.async_session() as session:
                week = HomeworkWeek1 if week_id == 1 else HomeworkWeek2

                query = await session.execute(
                    select(
                        week.week_id,
                        Day.day,
                        Subject.subject,
                        week.assignment,
                        week.image,
                    )
                    .join(Day, and_(week.day_id == Day.id, Day.id == day_id))
                    .join(Subject, week.subject_id == Subject.id)
                )
                query = query.fetchall()

                data = [
                    {
                        "week": week,
                        "day": day,
                        "subject": subject,
                        "assignment": assignment,
                        "image": image
                    } for week, day, subject, assignment, image in query
                ]

                # # printing data
                # formatted_data = '\n'.join([str(item) for item in data])
                # print(formatted_data)
                #
                # # printing subjects
                # subjects_list = [subject[2] for subject in query]
                # print(subjects_list)

                logger.log_info(f"{f'Homework retrieved successfully'.ljust(46)} ::")
                return data

        except SQLAlchemyError as exception:
            logger.log_error(f"{f'Failed to retrieve homework'.ljust(46)} :: {exception}")

    # --> SCHEDULED METHOD

    async def scheduled(self):
        try:
            async with self.async_session() as session:

                # Update HomeworkWeek1
                try:
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

                    logger.log_info(f"{'HomeworkWeek2 cleaned successfully'.ljust(46)} ::")

                except SQLAlchemyError as exception:
                    logger.log_error(f"{f'Failed to update HomeworkWeek1'.ljust(46)} :: {exception}")

                # Clean HomeworkWeek2
                try:
                    await session.execute(delete(HomeworkWeek2))

                    entry = [
                        HomeworkWeek2(
                            day_id=entry[0],
                            subject_id=entry[1],
                            subgroup_id=entry[2],
                            homework="",
                            image=""
                        )
                        for entry in schedule
                    ]
                    session.add_all(entry)
                    await session.commit()

                    logger.log_info(f"{'HomeworkWeek2 cleaned successfully'.ljust(46)} ::")

                except SQLAlchemyError as exception:
                    logger.log_error(f"{f'Failed to clean HomeworkWeek2'.ljust(46)} :: {exception}")

        except SQLAlchemyError as exception:
            logger.log_error(f"{f'Failed to execute scheduled task'.ljust(46)} :: {exception}")


database = Database()
