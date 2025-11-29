from rest_framework import viewsets
from .models import Player, Game, GamePlayer, Advertisement
from .serializers import PlayerSerializer, GameSerializer, GamePlayerSerializer, AdvertisementSerializer

# -----------------------------
# Игроки
# -----------------------------
class PlayerViewSet(viewsets.ModelViewSet):
    queryset = Player.objects.all()
    serializer_class = PlayerSerializer


# -----------------------------
# Игры
# -----------------------------
class GameViewSet(viewsets.ModelViewSet):
    queryset = Game.objects.all()
    serializer_class = GameSerializer


class GamePlayerViewSet(viewsets.ModelViewSet):
    queryset = GamePlayer.objects.all()
    serializer_class = GamePlayerSerializer


# -----------------------------
# Реклама
# -----------------------------
class AdvertisementViewSet(viewsets.ModelViewSet):
    queryset = Advertisement.objects.all()
    serializer_class = AdvertisementSerializer
