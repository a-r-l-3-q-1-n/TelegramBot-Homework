from sqlalchemy import ForeignKey, BigInteger, Index, Text
from sqlalchemy.ext.asyncio import AsyncAttrs
from sqlalchemy.orm import DeclarativeBase, Mapped
from sqlalchemy.orm import mapped_column


class Base(AsyncAttrs, DeclarativeBase):
    pass


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    telegram_id: Mapped[int] = mapped_column(BigInteger, nullable=False, unique=True)
    username: Mapped[str] = mapped_column(nullable=False)

    __table_args__ = (Index("ix_users_telegram_id", "telegram_id"),
                      Index("ix_users_username", "username"))


class Day(Base):
    __tablename__ = "days"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    day: Mapped[str] = mapped_column(nullable=False)


class Subject(Base):
    __tablename__ = "subjects"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    subject: Mapped[str] = mapped_column(nullable=False)


class HomeworkWeek1(Base):
    __tablename__ = "homeworkweek1"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    week_id: Mapped[int] = mapped_column()
    day_id: Mapped[int] = mapped_column(ForeignKey("days.id"), nullable=False)
    subject_id: Mapped[int] = mapped_column(ForeignKey("subjects.id"), nullable=False)
    assignment: Mapped[str] = mapped_column(Text, nullable=False)
    image: Mapped[str] = mapped_column(Text, nullable=False)


class HomeworkWeek2(Base):
    __tablename__ = "homeworkweek2"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    week_id: Mapped[int] = mapped_column(nullable=False)
    day_id: Mapped[int] = mapped_column(ForeignKey("days.id"), nullable=False)
    subject_id: Mapped[int] = mapped_column(ForeignKey("subjects.id"), nullable=False)
    assignment: Mapped[str] = mapped_column(Text, nullable=False)
    image: Mapped[str] = mapped_column(Text, nullable=False)
