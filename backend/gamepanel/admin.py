from django.contrib import admin
from api.models import Player, Game, GamePlayer, Advertisement

# Регистрируем модели для админки Django
admin.site.register(Player)
admin.site.register(Game)
admin.site.register(GamePlayer)
admin.site.register(Advertisement)
