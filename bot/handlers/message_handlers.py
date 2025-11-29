from telebot import types

def join_callback_handler(call, bot, games):
    chat_id = int(call.data.split("_")[1])
    user_name = call.from_user.first_name

    if chat_id not in games:
        bot.answer_callback_query(call.id, "Ошибка: группа не найдена.")
        return

    if user_name in games[chat_id]["players"]:
        bot.answer_callback_query(call.id, f"{user_name}, вы уже присоединились!")
        return

    # Добавляем игрока
    games[chat_id]["players"].append(user_name)
    bot.answer_callback_query(call.id, f"{user_name}, вы присоединились к игре!")

    # Обновляем сообщение с кнопкой и списком игроков
    markup = types.InlineKeyboardMarkup()
    join_button = types.InlineKeyboardButton("Присоединиться", callback_data=f"join_{chat_id}")
    markup.add(join_button)

    players_text = "\n".join(games[chat_id]["players"])
    bot.edit_message_text(chat_id=chat_id,
                          message_id=call.message.message_id,
                          text=f"🎵 Атмосфера: Chill\nИгроки:\n{players_text}",
                          reply_markup=markup)
