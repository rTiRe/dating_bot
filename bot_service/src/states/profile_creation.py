from aiogram.fsm.state import StatesGroup, State

class ProfileCreationStates(StatesGroup):
    name = State()
    age = State()
    gender = State()
    photo = State()
    city = State()
    interested_in = State()
    description = State()
    check = State()
