from aiogram.types import ReplyKeyboardMarkup,KeyboardButton

menu_user = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Магазин"),
            KeyboardButton(text="Корзина"),
        ],
        # [
        #     KeyboardButton(text="Пололнить счет")
        # ],
    ],
    resize_keyboard=True
)
admin_panel = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Добавить товар"),
            KeyboardButton(text="Оплаченые товары"),
        ],
        [
            KeyboardButton(text="Доступный товар"),
            KeyboardButton(text="Редактировать товар"),
        ],
        [
            KeyboardButton(text="Товар для отправки")
        ],
    ],
    resize_keyboard=True
)
done_add = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Готово"),
        ],
        [
          KeyboardButton(text="Отмена"),
        ],

    ],
    resize_keyboard=True
)
done_add1 = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Завершить"),
            KeyboardButton(text="Отмена"),
        ],

    ],
    resize_keyboard=True
)
cancel = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Отмена"),
        ],

    ],
    resize_keyboard=True
)
