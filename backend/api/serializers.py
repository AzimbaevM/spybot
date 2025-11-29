from rest_framework import serializers
from .models import Player, Game, GamePlayer, Advertisement

# -----------------------------
# Игроки
# -----------------------------
class PlayerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Player
        fields = '__all__'


# -----------------------------
# Игры
# -----------------------------
class GameSerializer(serializers.ModelSerializer):
    class Meta:
        model = Game
        fields = '__all__'


class GamePlayerSerializer(serializers.ModelSerializer):
    class Meta:
        model = GamePlayer
        fields = '__all__'


# -----------------------------
# Реклама
# -----------------------------
class AdvertisementSerializer(serializers.ModelSerializer):
    class Meta:
        model = Advertisement
        fields = '__all__'
