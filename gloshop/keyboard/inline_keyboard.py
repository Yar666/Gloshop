from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from .callback_data import *


# choice = InlineKeyboardMarkup(
#     inline_keyboard=[
#         [
#             InlineKeyboardButton(text='Купить',callback_data=buy_callback.new(
#                 item_name="pear",quantity=1
#             ))
#         ]
#     ]
# )
async def create_inline_keyboard(get_data, message, bot, menu_user):
    if not get_data:
        await message.answer('Магазин пуст', reply_markup=menu_user)
    for i in get_data:
        choice = InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    InlineKeyboardButton(text='Купить', callback_data=buy_callback.new(
                        item_name=i, quantity=1, cost=get_data[i]['cost']
                    ))
                ]
            ]
        )
        if get_data[i]["images"] != "":
            # await bot.send_photo(chat_id=message.from_user.id, photo=get_data[i]["images"])
            await message.answer_photo(photo=get_data[i]["url"],
                                       caption=str(get_data[i]['name']) + "\n" + str(get_data[i]['cost']),
                                       reply_markup=choice)
        else:
            await message.answer(str(get_data[i]['name']) + "\n" + str(get_data[i]['cost']), reply_markup=choice)
async def show_basket(get_data, message, bot, menu_user, db):
    if not db.get_basket(message.from_user.id, '*'):
        await message.answer("В Вашей корзине нет товаров")
    else:
        for i in db.get_basket(message.from_user.id, '*'):
            print(i)
            print(get_data)
            paid_ = [' Нет'
                     if i[3] == 0 else ' Да']
            choice = InlineKeyboardMarkup(
                inline_keyboard=[
                    [
                        InlineKeyboardButton(text='Удалить', callback_data=remove_callback.new(
                            autonum=i[0]
                        )),
                        InlineKeyboardButton(text='Опалить', callback_data=pay_callback.new(
                            autonum=i[0],item_name=get_data[i[2]]['hide_id']
                        ))
                    ]
                ]
            )
            if paid_[0] ==' Да':
                await message.answer("Описание товара:\n" + get_data[i[2]]['name'] +'\nЦена: '+get_data[i[2]]['cost']+ "\nОплачено:" +paid_[0]+
                                     '\nДата заказа: ' + i[4] + '\nКоличество: ' +
                                     str(i[5]))
            else:
                await message.answer("Описание товара:\n" + get_data[i[2]]['name'] +'\nЦена: '+get_data[i[2]]['cost']+ "\nОплачено:" +paid_[0]+
                                     '\nДата заказа: ' + i[4] + '\nКоличество: ' +
                                     str(i[5]),reply_markup=choice)
async def show_order(message, db):
    get_order = db.get_order()
    if not get_order:
        await message.answer("Еще никто ничего не заказал")
    for i in get_order:
        i = [str(j) for j in i]
        print(i)
        choice = InlineKeyboardMarkup(
                inline_keyboard=[
                    [
                        InlineKeyboardButton(text='Отправлено', callback_data=send_True.new(
                            autonum=i[0]
                        ))
                    ]
                ]
            )
        await message.answer('Id пользователя: '+i[1]+'\nИмя в телеграмм: '+i[2]+'\nЦена: '+i[3]+'\nНа имя: '+i[4]+'\nГород: '+i[5]+'\nУлица: '+i[6]+'\nОбласть: '+i[7]+'\nИндекс: '+i[8],reply_markup=choice)
