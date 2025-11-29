from django.db import models

# -----------------------------
# Игроки
# -----------------------------
class Player(models.Model):
    telegram_id = models.BigIntegerField(unique=True)
    username = models.CharField(max_length=64)
    money = models.IntegerField(default=100)
    gems = models.IntegerField(default=0)
    protection = models.IntegerField(default=0)
    documents = models.IntegerField(default=0)
    active_role = models.CharField(max_length=64, default="0")
    last_game = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.username} ({self.telegram_id})"


# -----------------------------
# Игры
# -----------------------------
class Game(models.Model):
    chat_id = models.BigIntegerField()
    topic = models.CharField(max_length=128)
    is_active = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    winner = models.CharField(max_length=32, blank=True, null=True)  # "spy" или "citizens"

    def __str__(self):
        return f"Game {self.chat_id} ({'active' if self.is_active else 'finished'})"


class GamePlayer(models.Model):
    game = models.ForeignKey(Game, on_delete=models.CASCADE, related_name="players")
    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    word = models.CharField(max_length=64)  # слово для игрока
    votes = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.player.username} in Game {self.game.chat_id}"


# -----------------------------
# Реклама
# -----------------------------
class Advertisement(models.Model):
    title = models.CharField(max_length=128)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.title
