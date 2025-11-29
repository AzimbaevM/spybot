import random

# Пары слов: (слово_жителя, слово_шпиона) — близкие по смыслу/форме
WORD_PAIRS = [
    ("ШЛЯПА", "КЕПКА"),
    ("КОМПАС", "МАЯК"),
    ("КАРАНДАШ", "Ручка".upper()),
    ("СТУЛ", "ТАБУРЕТ"),
    ("МОРЕ", "ОКЕАН"),
    ("ЯБЛОКО", "ГРУША"),
    ("КОФЕ", "ЧАЙ"),
    ("БИБЛИОТЕКА", "КНИЖНЫЙ ЗАЛ"),
    ("АЭРОПОРТ", "ТЕРМИНАЛ"),
    ("КАФЕ", "РЕСТОРАН"),
]

TOPICS = [
    "Школа", "Магазин", "Пляж", "Кинотеатр", "Больница",
    "Самолёт", "Кафе", "Стадион", "Банк", "Библиотека"
]

def get_random_topic():
    return random.choice(TOPICS)

def get_word_pair():
    return random.choice(WORD_PAIRS)

def format_player_list(players):
    return "\n".join([f"• @{p.username}" for p in players])
