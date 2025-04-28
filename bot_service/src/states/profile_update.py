from aiogram.fsm.state import StatesGroup, State

class ProfileUpdateStates(StatesGroup):
    name = State('name')
    age = State('age')
    gender = State('gender')
    photo = State('photo')
    city = State('city')
    interested_in = State('interested_in')
    description = State('description')
    check = State('check')
