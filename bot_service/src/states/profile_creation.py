from aiogram.fsm.state import StatesGroup, State

class ProfileCreationStates(StatesGroup):
    name = State('name')
    age = State('age')
    gender = State('gender')
    photo = State('photo')
    city = State('city')
    interested_in = State('interested_in')
    description = State('description')
    check = State('check')
