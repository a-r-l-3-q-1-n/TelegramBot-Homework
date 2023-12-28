from aiogram.fsm.state import StatesGroup, State


class AddUser(StatesGroup):
    USERNAME: str = State()


class Support(StatesGroup):
    MESSAGE: str = State()


class ViewHW(StatesGroup):
    WEEK: int = State()


class UploadHW(StatesGroup):
    WEEK = State()
    DAY = State()
    SUBJECT = State()
    ASSIGNMENT: str = State()
    IMAGE: str = State()
