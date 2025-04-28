from aiogram.fsm.state import StatesGroup, State

class MainStates(StatesGroup):
    default = State('default')
    menu = State('main')
    search = State('search')
