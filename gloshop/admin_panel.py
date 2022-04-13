from aiogram import types

from bot.telegram.gloshop.Things.json_helper import loadjson
from main import dp, bot, db
from aiogram.dispatcher.filters import Text, Command
from keyboard.keyboard import admin_panel, cancel
from Things.some_add import AskForAdd, AskForRename
from keyboard.inline_keyboard import show_order
import filtres



async def notify_for_admin(id,bot):
    await bot.send_message(id,"Пришел заказ")

@dp.message_handler(Command('admin'),is_admin=True)
async def administratot(message):
    await message.answer('Панель Андминистратора.\nДля выхода /user', reply_markup=admin_panel)


@dp.message_handler(Text('Добавить товар'), user_id=[i[0] for i in db.get_admins()])
async def enter_test(message: types.Message):
    await message.answer("Добавление в каталог\n"
                         "Опишите товар. Пример:\nГло про\nЦена 200 грн\nЦвет на выбор\nВнимание цена в описании должна быть равна цене в системе", reply_markup=cancel)
    await AskForAdd.Q1.set()


@dp.message_handler(Text('Оплаченые товары'), user_id=[i[0] for i in db.get_admins()])
async def paid_thing(message: types.Message):
    paid = db.get_basket(message.from_user.id, 'paid')
    print(paid)
    if not paid:
        await message.answer("Еще никто ничего не купил")
    else:
        get_data = loadjson("catalog.json")
        # if not get_data:
        #     await message.answer('Магазин пуст', reply_markup=admin_panel)
        # else:
        print(get_data)
        for i in paid:
            await message.answer("Id покупателя: " + str(i[1]) + '\n' + 'Описание товара:\n' + ['Такого товара больше не существует' if not get_data else get_data[i[2]]['name']][0] + '\n' + "Количество " + str(i[5]) + '\n' + 'Дата заказа ' + str(i[4]))


@dp.message_handler(Text('Доступный товар'), user_id=[i[0] for i in db.get_admins()])
async def paid_thing(message: types.Message):
    get_data = loadjson("catalog.json")
    print(get_data)
    if not get_data:
        await message.answer('Магазин пуст', reply_markup=admin_panel)
    for i in get_data:
        await message.answer('name: \n'+str(get_data[i]['name']) + "\n" + 'cost: \n'+str(get_data[i]['cost']) + '\n' + "Скрытый id: " + str(
            get_data[i]['hide_id']))


@dp.message_handler(Text('Редактировать товар'), user_id=[i[0] for i in db.get_admins()])
async def paid_thing(message: types.Message):
    await message.answer("Укажите скрытый id товара.", reply_markup=cancel)
    await AskForRename.Q1.set()
@dp.message_handler(Text('Товар для отправки'), user_id=[i[0] for i in db.get_admins()])
async def paid_thing(message: types.Message):
    await show_order(message,db)
