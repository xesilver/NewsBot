from aiogram import Bot, Dispatcher, executor, types
from NewsBot import keyboards as kb

# from NewsBot import DB as DB


# load_dotenv()
bot = Bot('')
dp = Dispatcher(bot=bot)


# async def on_startup(_):
#     await DB.db_start()
#     print('Bot started')


@dp.message_handler(commands=['start'])
async def cmd_start(message: types.Message):
    # await DB.cmd_start_db(message.from_user.id)
    await message.answer_sticker("CAACAgIAAxkBAAEJSLhkhg9u4WMMnU5OnMNxfzubgXcaTwACKRUAAviLwEupQBIzh-Q46C8E")
    if message.from_user.id == :
        await message.answer(f"Welcome, admin!", reply_markup=kb.main_admin)
    else:
        await message.answer(f"Welcome, {message.from_user.first_name}", reply_markup=kb.main)


@dp.message_handler(text='Politics')
async def catalogue(message: types.Message):
    await message.reply(f"Choose broadcaster", reply_markup=kb.politic_list)


@dp.message_handler(text='Sports')
async def cart(message: types.Message):
    await message.reply(f'Choose broadcaster', reply_markup=kb.sports_list)


@dp.message_handler(text='Games')
async def contacts(message: types.Message):
    await message.reply(f'Choose broadcaster', reply_markup=kb.games_list)


@dp.message_handler(text='admin_panel')
async def admin_panel(message: types.Message):
    if message.from_user.id == :
        await message.reply(f"You have opened admin_panel", reply_markup=kb.admin_keyboard)
    else:
        await message.reply(f"Stop this")


@dp.message_handler(text='return')
async def admin_return(message: types.Message):
    if message.from_user.id == :
        await message.reply(f"return", reply_markup=kb.main_admin)
    else:
        await message.reply(f"If you are confused, use /help")


# @dp.message_handler(commands=['id'])
# async def cmd_start(message: types.Message):
#     await message.answer(message.from_user.id)


@dp.message_handler()
async def response(message: types.Message):
    await message.reply(f"If you are confused, use /help")


# @dp.callback_query_handler()
# async def callback_query_keyboard(callback_query: types.CallbackQuery):
#     if callback_query.data == "One":
#         await bot.send_message(chat_id=callback_query.from_user.id, text="You picked one")
#     elif callback_query.data == "Two":
#         await bot.send_message(chat_id=callback_query.from_user.id, text="You picked two")
#     elif callback_query.data == "Three":
#         await bot.send_message(chat_id=callback_query.from_user.id, text="You picked three")


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
# on_startup=on_startup
