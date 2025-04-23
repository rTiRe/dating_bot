from aiogram.fsm.state import StatesGroup, State

class ProfileCreationStates(StatesGroup):
    name = State()
    age = State()
    sex = State()
    photo = State()
    city = State()
    sex_preferences = State()
    description = State()
    check = State()
