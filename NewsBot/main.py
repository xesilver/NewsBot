from aiogram import Bot, Dispatcher, executor, types
import keyboards as kb
from multiprocessing import Process
import asyncio
from config import TOKEN
import parser
import db


bot = Bot(TOKEN)
dp = Dispatcher(bot=bot)
connection = db.DbConnection()


@dp.message_handler(commands=['start'])
async def cmd_start(message: types.Message):
    await bot.send_animation(chat_id=message.chat.id, animation=open(r'...\media\greeting_gif.mp4', 'rb'))
    await message.answer(f"Welcome, {message.from_user.first_name}!", reply_markup=kb.main_keyboard)


@dp.message_handler(commands=['help'])
async def show_help(message: types.Message):
    await message.answer(
        'This bot was created to help you to know the actual global situation. We provide many authoritative sources '
        'of information on any topic you like. This is free of charge. \n\nTo start using the bot, use button menu '
        'under this message and choose the type of news you want to receive. After that the bot will reply you with '
        'available newspapers. Choose one and obtain all the information that was published for the last time.'
        ,
        reply_markup=kb.main_keyboard)


@dp.message_handler(text='Politics')
async def show_politics(message: types.Message):
    await message.reply(f"Choose broadcaster", reply_markup=kb.politic_list)


@dp.message_handler(text='Sports')
async def show_sports(message: types.Message):
    await message.reply(f'Choose broadcaster', reply_markup=kb.sports_list)


@dp.message_handler(text='Games')
async def show_games(message: types.Message):
    await message.reply(f'Choose broadcaster', reply_markup=kb.games_list)


@dp.message_handler()
async def show_incorrectness(message: types.Message):
    await message.reply(f"If you are confused, use /help")


# Function which is run in a new thread and creates a final formatted message which will be sent to the user.
def create_message(db_news: list) -> str:
    message = ''

    for section in db_news:
        message += f'• <a href="{section.get("link")}">{section.get("article")}</a>\n\n'

    return message


@dp.callback_query_handler()
async def callback_query_keyboard(callback_query: types.CallbackQuery):
    await connection.create_pool()
    db_news = await connection.get_news(callback_query.data)

    message = await asyncio.to_thread(create_message, db_news)

    await bot.send_message(callback_query.from_user.id, text=f'{message}', parse_mode='HTML',
                           disable_web_page_preview=True)


# Function which is run in a new process and runs `main()` function from module `parser`.
def start_parsing():
    asyncio.run(parser.main())


if __name__ == '__main__':
    Process(target=start_parsing).start()
    executor.start_polling(dp, skip_updates=True)
