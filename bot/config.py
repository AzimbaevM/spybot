import os
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("BOT_TOKEN")
if not TOKEN:
    raise ValueError("BOT_TOKEN не найден в .env")

# ID админа(ов) через запятую в .env, например: ADMINS=123,456
ADMINS = [int(x) for x in os.getenv("ADMINS", "").split(",") if x.strip().isdigit()]

# Путь к ассетам (только музыка)
BASE_DIR = os.path.dirname(__file__)
ASSETS_PATH = os.path.join(BASE_DIR, "assets")

# Файлы музыки (имена файлов в папке assets)
BACKGROUND_TRACKS = ["bg1.mp3", "bg2.mp3", "bg3.mp3", "bg4.mp3", "bg5.mp3"]

# Идентификатор администратора рассылок (один id можно)
SUPER_ADMIN = int(os.getenv("SUPER_ADMIN", "0")) if os.getenv("SUPER_ADMIN") else None

# Параметры игры
MIN_PLAYERS = int(os.getenv("MIN_PLAYERS", "3"))
SPEECH_TIME = int(os.getenv("SPEECH_TIME", "60"))   # секунды на ход
VOTE_TIME = int(os.getenv("VOTE_TIME", "60"))       # секунды на голосование
AUTO_NEXT_GAME_DELAY = int(os.getenv("AUTO_NEXT_GAME_DELAY", "60"))  # сек до новой игры
