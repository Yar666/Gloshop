from aiogram.utils.callback_data import CallbackData

buy_callback = CallbackData("buy","item_name","quantity","cost")
remove_callback = CallbackData("remove","autonum")
pay_callback = CallbackData("pay","autonum","item_name")
send_True = CallbackData("send","autonum")
