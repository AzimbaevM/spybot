from telebot import types

def start_game(message, bot, games):
    chat_id = message.chat.id

    # Проверяем, что это группа
    if message.chat.type not in ['group', 'supergroup']:
        bot.send_message(chat_id, "Добавьте меня в группу, чтобы начать игру!")
        return

    # Инициализация группы
    if chat_id not in games:
        games[chat_id] = {
            "players": [],
            "status": "waiting"
        }

    # Кнопка Join
    markup = types.InlineKeyboardMarkup()
    join_button = types.InlineKeyboardButton("Присоединиться", callback_data=f"join_{chat_id}")
    markup.add(join_button)

    bot.send_message(chat_id,
                     "🎵 Атмосфера: Chill\nНажмите 'Присоединиться', чтобы вступить в игру!",
                     reply_markup=markup)
