from aiogram import types
from aiogram.dispatcher.filters import BoundFilter
from main import db, dp

class MyFilterr(BoundFilter):
    key = 'is_admin'

    def __init__(self, is_admin):
        self.is_admin = is_admin

    async def check(self, message: types.Message):
        admins = [i[0] for i in db.get_admins()]
        if message.from_user.id in admins:
            return True
        else:
            return False
dp.filters_factory.bind(MyFilterr)
