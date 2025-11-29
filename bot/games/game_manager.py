import random
import threading
from collections import defaultdict
from .player import GamePlayer
from .utils import get_random_topic, get_word_pair
from config import SPEECH_TIME, VOTE_TIME, MIN_PLAYERS

class GameManager:
    def __init__(self, chat_id, bot):
        self.chat_id = chat_id
        self.bot = bot
        self.players = []  # list[GamePlayer]
        self.spies = []    # list of GamePlayer (1..n)
        self.topic = None
        self.word_citizen = None
        self.word_spy = None
        self.is_active = False
        self.current_speaker_index = 0
        self.phase = "idle"  # idle, speaking, voting
        self.votes = defaultdict(int)
        self.timer = None
        self.lock = threading.Lock()

    def add_player(self, tg_id, username):
        if any(p.tg_id == tg_id for p in self.players):
            return False
        self.players.append(GamePlayer(tg_id, username))
        return True

    def remove_player(self, tg_id):
        self.players = [p for p in self.players if p.tg_id != tg_id]

    def start_game(self):
        with self.lock:
            if len(self.players) < MIN_PLAYERS:
                return False, f"Нужно минимум {MIN_PLAYERS} игроков."
            # подготовка
            self.is_active = True
            self.topic = get_random_topic()
            pair = get_word_pair()
            self.word_citizen, self.word_spy = pair
            # определить количество шпионов: ceil(n/4)
            n = len(self.players)
            spies_count = max(1, (n + 3) // 4)
            self.spies = random.sample(self.players, spies_count)
            for p in self.players:
                if p in self.spies:
                    p.role = "spy"
                    p.word = self.word_spy
                else:
                    p.role = "citizen"
                    p.word = self.word_citizen
                p.reset_for_round()
            self.current_speaker_index = 0
            self.phase = "speaking"
            # уведомления в ЛС — отдельно отправятся
            return True, f"Игра началась! Тема: {self.topic}. Игроков: {len(self.players)}. Раунд начинается."

    def get_player_by_tg(self, tg_id):
        for p in self.players:
            if p.tg_id == tg_id:
                return p
        return None

    def all_spoken(self):
        return all(p.spoken or not p.is_active for p in self.players)

    def start_next_speech(self):
        with self.lock:
            # найти следующего активного, кто ещё не говорил
            while self.current_speaker_index < len(self.players):
                p = self.players[self.current_speaker_index]
                self.current_speaker_index += 1
                if p.is_active and not p.spoken:
                    # запускаем таймер
                    self.phase = "speaking"
                    self.timer = threading.Timer(SPEECH_TIME, self._speech_timeout, args=(p.tg_id,))
                    self.timer.start()
                    return p
            # если дошли до конца
            return None

    def _speech_timeout(self, tg_id):
        # таймаут на говорение - помечаем как сказанного и двигаем дальше
        p = self.get_player_by_tg(tg_id)
        if p:
            p.spoken = True
        # продолжить раунд в основном потоке обработчика
        # (основной код должен вызвать check_after_speech)
        try:
            self.bot.send_message(self.chat_id, f"⏱ Время игрока @{p.username} окончено.")
        except Exception:
            pass

    def end_speech_for_player(self, tg_id):
        # если игрок досрочно закончил (нажал кнопку или написал правильно), отменяем таймер
        with self.lock:
            if self.timer:
                self.timer.cancel()
                self.timer = None
            p = self.get_player_by_tg(tg_id)
            if p:
                p.spoken = True

    def start_voting(self):
        with self.lock:
            self.phase = "voting"
            self.votes = defaultdict(int)
            # можно запустить таймер для голосования
            self.timer = threading.Timer(VOTE_TIME, self._vote_timeout)
            self.timer.start()

    def _vote_timeout(self):
        # по истечении голосования считаем результаты
        try:
            self.bot.send_message(self.chat_id, "⏱ Время голосования закончилось.")
        except Exception:
            pass
        self.finish_voting()

    def cast_vote(self, voter_tg, target_username):
        with self.lock:
            voter = self.get_player_by_tg(voter_tg)
            if not voter or not voter.is_active:
                return False, "Вы не участвуете в игре."
            target = next((p for p in self.players if p.username.lower() == target_username.lower()), None)
            if not target:
                return False, "Игрок не найден."
            self.votes[target.username] += 1
            return True, f"Голос за @{target.username} учтён."

    def finish_voting(self):
        with self.lock:
            if self.timer:
                self.timer.cancel()
                self.timer = None
            if not self.votes:
                self.bot.send_message(self.chat_id, "Никто не проголосовал — никто не исключён.")
                # сброс и следующий раунд
                self._prepare_next_round()
                return
            # подсчёт
            sorted_votes = sorted(self.votes.items(), key=lambda x: x[1], reverse=True)
            top_name, top_votes = sorted_votes[0]
            # проверка на ничью
            tied = [name for name, v in sorted_votes if v == top_votes]
            if len(tied) > 1:
                self.bot.send_message(self.chat_id, f"Ничья между: {', '.join(tied)}. Никто не исключён.")
                self._prepare_next_round()
                return
            # исключаем игрока
            target = next((p for p in self.players if p.username == top_name), None)
            if target:
                target.is_active = False
                self.bot.send_message(self.chat_id, f"🚪 @{target.username} исключён из игры (не может больше говорить).")
            # проверка победы
            self._check_victory_conditions()
            # подготовка следующего раунда, если игра не окончена
            if self.is_active:
                self._prepare_next_round()

    def _prepare_next_round(self):
        # сброс для следующего раунда
        for p in self.players:
            p.reset_for_round()
        self.current_speaker_index = 0
        self.phase = "speaking"
        # можно автоматом запустить следующий раунд или ждать /start_round
        # здесь просто уведомим
        self.bot.send_message(self.chat_id, "➡️ Новый раунд начинается. Говорит следующий игрок.")
        # автоматически запускаем следующий спик
        next_p = self.start_next_speech()
        if next_p:
            try:
                self.bot.send_message(self.chat_id, f"Сейчас ход: @{next_p.username} (1 мин).")
                # отправляем ЛС слово игроку
                try:
                    self.bot.send_message(next_p.tg_id, f"Твое слово (тайно): {next_p.word}")
                except Exception:
                    pass
            except Exception:
                pass

    def _check_victory_conditions(self):
        # считаем активные шпионов и активных мирных
        active_spies = [p for p in self.spies if p.is_active]
        active_citizens = [p for p in self.players if p.is_active and p not in self.spies]
        if len(active_spies) == 0:
            # мирные победили
            self.bot.send_message(self.chat_id, "🏅 Мирные победили!")
            self.is_active = False
            return
        # если шпионов >= мирных
        if len(active_spies) >= len(active_citizens):
            self.bot.send_message(self.chat_id, "🕵️‍♀️ Шпионы победили!")
            self.is_active = False
            return
