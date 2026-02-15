from aiogram.fsm.state import State, StatesGroup

class LinkAccount(StatesGroup):
    waiting_for_code = State()