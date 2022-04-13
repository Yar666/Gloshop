from aiogram import types
from aiogram.dispatcher import FSMContext
from bot.telegram.gloshop import states
from main import bot, dp, db
from datetime import datetime, timedelta
from aiogram.types import Message, CallbackQuery, LabeledPrice, PreCheckoutQuery
from aiogram.dispatcher.filters import Command, Text
from keyboard.keyboard import *
from Things.json_helper import loadjson
from config import *
from keyboard.inline_keyboard import create_inline_keyboard, show_basket
from bot.telegram.gloshop.keyboard.callback_data import buy_callback
import admin_panel
from admin_panel import notify_for_admin

async def send_to_admin(f):
    await bot.send_message(chat_id=779032981, text="Бот запущен", reply_markup=menu_user)


@dp.message_handler(content_types=['photo'])
async def handle_docs_photo(message):
    if message.photo:
        # print(message)
        document = message.photo[-1]
        # url = bot.get_file(document)
        # print(document.file_id)
        # await message.answer_photo(photo="file_5.jpg",caption='s')
        # await document.download(destination_dir='Things/Images/')
        file_info = await bot.get_file(document.file_id)
        print(file_info["file_id"])
        await message.answer_photo(photo=file_info["file_id"],caption='s')
        # print(f'file_path: {file_info.file_path}')
@dp.message_handler(Command(['get_admin']))
async def get_admin(message: Message):
    await message.answer("Вам выдана андим панель. Для использования /admin")
    db.set_admin(message.from_user.id)
@dp.message_handler(Command(['menu', 'start','user']))
async def echo(message: Message):
    print(message)
    if not db.user_exists(message.from_user.id):
        db.add_user(message.from_user.id, message.from_user.first_name, message.from_user.last_name,
                    datetime.today() - timedelta(1))
    print(message.from_user.id)
    await message.answer("Вас приветствует магазин GloShop\n"
                         "Краткая информация\n"
                         f"Имя: {db.get_user(message.from_user.id, 'name')}\nФамилия: {db.get_user(message.from_user.id, 'surname')}",
                         # f"\nБаланс: {db.get_user(message.from_user.id, 'balance')} грн\n",
                         reply_markup=menu_user)


@dp.message_handler(Text('Магазин'))
async def shop(message):
    get_data = loadjson("catalog.json")
    print(get_data)
    await create_inline_keyboard(get_data, message, bot, menu_user)
    # for i in get_data:
    #     # if get_data[i]["images"] !="":
    #     #     await message.answer(get_data[i]['images'])
    #     await message.answer(str(get_data[i]['name'])+"\n"+str(get_data[i]['cost']))

@dp.message_handler(Text('Корзина'))
async def basket(message: types.Message):
    get_data = loadjson("catalog.json")
    await show_basket(get_data,message,bot,menu_user,db)


@dp.callback_query_handler(text_contains="buy")
async def buy_glo(call: CallbackQuery):
    await call.answer()
    callback_data = call.data.replace(":", ' ').split()
    print(call.data)
    db.add_thing(call.from_user.id, callback_data[1], datetime.today() - timedelta(1), cost=callback_data[3])
    await call.message.answer("Товар добавлен в корзину")
@dp.callback_query_handler(text_contains="send")
async def buy_glo(call: CallbackQuery):
    await call.answer(cache_time=120)
    callback_data = call.data.replace(":", ' ').split()
    await call.message.answer("Товар был успешно добавлен, пользователь уведомлен.")
    print(db.get_id(callback_data[1]))
    await bot.send_message(db.get_id(callback_data[1]),"Ваш товар отправлен")
    db.successful_send(callback_data[1])

@dp.callback_query_handler(text_contains="remove")
async def buy_glo(call: CallbackQuery):
    await call.answer(cache_time=120)
    callback_data = call.data.replace(":", ' ').split()
    await bot.delete_message(chat_id=call.from_user.id, message_id=call.message.message_id)
    print(callback_data)
    db.delete_basket(call.from_user.id,callback_data[1])
    await call.message.answer("Товар удален из корзины")
@dp.callback_query_handler(text_contains="pay")
async def buy_glo(call: CallbackQuery):
    await call.answer(cache_time=120)
    callback_data = call.data.replace(":", ' ').split()
    get_data = loadjson("catalog.json")
    print(callback_data)
    # await call.message.answer(get_data[callback_data[2]]['name'])
    currency = "UAH"
    need_name = True
    need_phone_number = False
    need_email = False
    need_shipping_address = True
    PRICE = types.LabeledPrice(label='Настоящая Машина Времени', amount=20000)
    await bot.send_invoice(chat_id=call.from_user.id,
                           title="Оплата",
                           description=get_data[callback_data[2]]['name'],
                           payload='some-invoice-payload-for-our-internal-use',
                           start_parameter='test',
                           currency=currency,
                           prices=[PRICE],
                           provider_token='632593626:TEST:sandbox_i30056585195',
                           need_name=need_name,
                           need_phone_number=need_phone_number,
                           need_email=need_email,
                           need_shipping_address=need_shipping_address
                           )
    states.Purchase.Autonum = callback_data[1]
    await states.Purchase.Payment.set()
@dp.pre_checkout_query_handler(state=states.Purchase.Payment)
async def checkout(query: PreCheckoutQuery, state:FSMContext):
    await bot.answer_pre_checkout_query(query.id, True)
    success = await check_payment()
    if success:
        await bot.send_message(query.from_user.id, "Спасибо за покупку")
        await state.reset_state()
        db.successful_pay(states.Purchase.Autonum)
        print(query)
        if not query.order_info.shipping_address.street_line2:
            adress_line = query.order_info.shipping_address.street_line1
        else:
            adress_line = query.order_info.shipping_address.street_line2
        db.add_order(query.from_user.id,query.from_user.first_name,query.total_amount/100,query.order_info.name,query.order_info.shipping_address.city,adress_line,query.order_info.shipping_address.state,query.order_info.shipping_address.post_code)
        await notify_for_admin(query.from_user.id, bot)
async def check_payment():
    return True
