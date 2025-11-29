class GamePlayer:
    def __init__(self, tg_id: int, username: str):
        self.tg_id = tg_id
        self.username = username
        self.role = None            # "spy" или "citizen"
        self.word = None            # слово, которое игрок получает
        self.is_active = True       # участвует в игре (не исключён)
        self.votes = 0
        self.spoken = False         # уже говорил в раунде?

    def reset_for_round(self):
        self.votes = 0
        self.spoken = False

    def __repr__(self):
        return f"<GamePlayer @{self.username} ({self.role})>"
