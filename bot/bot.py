import os
import telebot
from telebot import types
from dotenv import load_dotenv
from handlers.message_handler import join_callback
from handlers.command_handler import start_command  # если есть функция start_command

# Загружаем .env
load_dotenv()
TOKEN = os.getenv("BOT_TOKEN")

bot = telebot.TeleBot(TOKEN)

# Словарь для хранения игроков по группам
games = {}

# --- Команда /start ---
@bot.message_handler(commands=['start'])
def start_game(message):
    chat_id = message.chat.id

    # Проверяем, что это группа
    if message.chat.type not in ['group', 'supergroup']:
        bot.send_message(chat_id, "Добавьте меня в группу, чтобы начать игру!")
        return

    # Инициализация группы в словаре
    if chat_id not in games:
        games[chat_id] = {
            "players": [],
            "status": "waiting"
        }

    # Создаем клавиатуру с кнопкой Join
    markup = types.InlineKeyboardMarkup()
    join_button = types.InlineKeyboardButton("Присоединиться", callback_data=f"join_{chat_id}")
    markup.add(join_button)

    bot.send_message(chat_id,
                     "🎵 Атмосфера: Chill\nНажмите 'Присоединиться', чтобы вступить в игру!",
                     reply_markup=markup)

# --- Callback для кнопки Join ---
@bot.callback_query_handler(func=lambda call: call.data.startswith("join_"))
def join_callback_handler(call):
    join_callback(call, bot, games)

# Запуск бота
if __name__ == "__main__":
    print("Бот запущен...")
    bot.infinity_polling()

    