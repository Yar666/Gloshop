
from aiogram.dispatcher.filters.state import StatesGroup, State


class Purchase(StatesGroup):
    Autonum=0
    EnterQuantity = State()
    Approval = State()
    Payment = State()
