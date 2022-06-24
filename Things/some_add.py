from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram import types
from aiogram.dispatcher import FSMContext
from main import dp, bot
from .json_helper import dumpjson, loadjson
from keyboard.keyboard import *

get_data = loadjson("catalog.json")


async def chech_answer(data, message):
    await message.answer("Убедитесь, что данные введены верно", reply_markup=done_add1)
    await message.answer(data.get('answer1') + "\n" + data.get('answer2') + "\n" + data.get(
        'answer3') + "\n(Если есть путь то фото успешно скачалось)")


class AskForAdd(StatesGroup):
    Q1 = State()
    Q2 = State()
    Q3 = State()
    Q4 = State()


class AskForRename(StatesGroup):
    Q1 = State()
    Q2 = State()
    name = State()
    cost = State()

@dp.message_handler(state=AskForRename.Q1)
async def answer_rename_q1(message: types.Message, state: FSMContext):
    answer = message.text
    if answer =='Отмена':
        await state.finish()
        await message.answer('Панель Андминистратора.\nДля выхода /user', reply_markup=admin_panel)
    else:
        if not answer.isdigit():
            await message.answer("Допустимы только числовые значения")
            await AskForRename.Q1.set()
        else:
            if len(get_data)<int(answer):
                await message.answer("Нет такого id")
                await AskForRename.Q1.set()
            else:
                await message.answer("Какой параметр изменить? Что бы удалить товар из каталога - remove", reply_markup=cancel)
                async with state.proxy() as data:
                    data['id']=answer
                await AskForRename.Q2.set()

@dp.message_handler(state=AskForRename.Q2)
async def answer_rename_q1(message: types.Message, state: FSMContext):
    answer = message.text
    if answer == 'Отмена':
        await state.finish()
        await message.answer('Панель Андминистратора.\nДля выхода /user', reply_markup=admin_panel)
    else:
        if answer =='remove':
            data = await state.get_data()
            print(get_data)
            # for i in range(1,len(get_data)+1):
            #     print(get_data[str(i)])
            # for i in range(len(get_data)):
            #     print(get_data[i])
            get_data.pop(str(data.get('id')))
            dumpjson(get_data, "catalog.json")
            await message.answer("Товар удален", reply_markup=admin_panel)
            await state.finish()
        elif answer == 'name':
            await message.answer("Опишите товар", reply_markup=cancel)
            await AskForRename.name.set()
        elif answer =='cost':
            await message.answer("Укажите цену", reply_markup=cancel)
            await AskForRename.cost.set()

@dp.message_handler(state=AskForRename.cost)
async def answer_cost(message: types.Message, state: FSMContext):
    answer = message.text
    if message.text == 'Отмена':
        await state.finish()
        await message.answer('Панель Андминистратора.\nДля выхода /user', reply_markup=admin_panel)
    else:
        if answer.isstates.Purchase.Autonumdigit():
            async with state.proxy() as data:
                data['cost']=answer
            data = await state.get_data()
            get_data[data.get('id')]['cost']=int(data.get('cost'))
            dumpjson(get_data, "catalog.json")
            await message.answer("Товар успешно редактирован", reply_markup=admin_panel)
            await state.finish()
        else:
            await message.answer("Допустимы только числовые значения", reply_markup=cancel)
            await AskForRename.cost.set()

@dp.message_handler(state=AskForRename.name)
async def answer_name(message: types.Message, state: FSMContext):
    answer = message.text
    if message.text == 'Отмена':
        await state.finish()
        await message.answer('Панель Андминистратора.\nДля выхода /user', reply_markup=admin_panel)
    else:
        async with state.proxy() as data:
            data['name']=answer
        data = await state.get_data()
        get_data[data.get('id')]['name']=str(data.get('name'))
        dumpjson(get_data, "catalog.json")
        await message.answer("Товар успешно редактирован", reply_markup=admin_panel)
        await state.finish()


@dp.message_handler(state=AskForAdd.Q1)
async def answer_q1(message: types.Message, state: FSMContext):
    answer = message.text
    print(answer)
    if message.text == 'Отмена':
        await state.finish()
        await message.answer('Панель Андминистратора.\nДля выхода /user', reply_markup=admin_panel)
    else:
        async with state.proxy() as data:
            data['answer1'] = answer
        await message.answer("Укажите цену в гривнах", reply_markup=cancel)
        await AskForAdd.Q2.set()


@dp.message_handler(state=AskForAdd.Q2)
async def answer_q2(message: types.Message, state: FSMContext):
    answer = message.text
    try:
        if message.text == 'Отмена':
            await state.finish()
            await message.answer('Панель Андминистратора.\nДля выхода /user', reply_markup=admin_panel)
        else:
            if not answer.isdigit():
                await message.answer("Допустимы только числовые значения", reply_markup=cancel)
                await AskForAdd.Q2.set()
            else:
                async with state.proxy() as data:
                    data['answer2'] = answer
                await message.answer("Добавьте картинку(не обязвательно).", reply_markup=done_add)
                await AskForAdd.Q3.set()
    except Exception as e:
        await message.answer(e)


@dp.message_handler(state=AskForAdd.Q3, content_types=types.ContentTypes.ANY)
async def answer_q3(message: types.Message, state: FSMContext):
    if message.text == 'Отмена':
        await state.finish()
        await message.answer('Панель Андминистратора.\nДля выхода /user', reply_markup=admin_panel)
    else:
        if message.text == 'Готово':
            async with state.proxy() as data:
                data['answer3'] = ""
            data = await state.get_data()
            await chech_answer(data, message)
            await AskForAdd.Q4.set()
        elif message.photo:
            document = message.photo[-1]
            await document.download(destination_dir='Things/Images/')
            file_info = await bot.get_file(document.file_id)
            print(f'file_path: {file_info.file_path}')
            async with state.proxy() as data:
                data['answer3'] = "Things/Images/" + file_info.file_path
                data['answer4'] = file_info["file_id"]
            data = await state.get_data()
            await chech_answer(data, message)
            await AskForAdd.Q4.set()


@dp.message_handler(state=AskForAdd.Q4)
async def answer_q4(message: types.Message, state: FSMContext):
    if message.text == 'Отмена':
        await state.finish()
        await message.answer('Панель Андминистратора.\nДля выхода /user', reply_markup=admin_panel)
    else:
        if message.text == "Завершить":
            data = await state.get_data()
            for i in get_data:
                print(get_data[i]['name'])
            get_data[len(get_data) + 1] = {"name": '{}'.format(data.get("answer1")),
                                           "cost": '{}'.format(data.get("answer2")),
                                           "images": '{}'.format(data.get("answer3")),
                                           "url": '{}'.format(data.get("answer4")),
                                           "hide_id": '{}'.format(len(get_data) + 1)}
            dumpjson(get_data, "catalog.json")
            await message.answer("Товар добавлен", reply_markup=menu_user)
            await state.finish()
