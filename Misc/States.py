from aiogram.fsm.state import StatesGroup, State


class RegisterUser(StatesGroup):
    NAME = State()


class SupportRequest(StatesGroup):
    MESSAGE = State()


class GetHW(StatesGroup):
    WEEK = State()


class AddHW(StatesGroup):
    ASSIGNMENT = State()
    IMAGE = State()
