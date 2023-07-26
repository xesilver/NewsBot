from aiogram.types import ReplyKeyboardMarkup, InlineKeyboardMarkup, InlineKeyboardButton

main_keyboard = ReplyKeyboardMarkup(resize_keyboard=True, input_field_placeholder='Choose a genre')
main_keyboard.add('Politics').add('Sports').add('Games')

politic_list = InlineKeyboardMarkup(row_width=2)
politic_list.add(InlineKeyboardButton(text="Politico", callback_data="politico"),
                 InlineKeyboardButton(text="Voanews", callback_data="voanews"),
                 InlineKeyboardButton(text="RT", callback_data="rt"),
                 InlineKeyboardButton(text="BBC", callback_data="bbc"),
                 InlineKeyboardButton(text="CNN", callback_data="cnn"),
                 InlineKeyboardButton(text="EuroNews", callback_data="euronews"))

sports_list = InlineKeyboardMarkup(row_width=2)
sports_list.add(InlineKeyboardButton(text="Guardiansport", callback_data="guardiansport"),
                InlineKeyboardButton(text="Skysports", callback_data="skysports"),
                InlineKeyboardButton(text="Sportingnews", callback_data="sportingnews"),
                InlineKeyboardButton(text="Deadspin", callback_data="deadspin"),
                InlineKeyboardButton(text="Euronews Sports", callback_data="euronews_sport"),
                InlineKeyboardButton(text="CNN Sports", callback_data="cnn_sports"))

games_list = InlineKeyboardMarkup()
games_list.add(InlineKeyboardButton(text="Thegamer", callback_data="thegamer"),
               InlineKeyboardButton(text="Stopgame", callback_data="stopgame"),
               InlineKeyboardButton(text="Xfire", callback_data="xfire"),
               InlineKeyboardButton(text="VG247", callback_data="vg247"),
               InlineKeyboardButton(text="Kotaku", callback_data="kotaku"))
