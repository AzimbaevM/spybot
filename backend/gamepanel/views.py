from django.shortcuts import render
from api.models import Player, Game, Advertisement

# def dashboard(request):
#     players = Player.objects.all()
#     games = Game.objects.all().order_by('-created_at')[:10]  # последние 10 игр
#     ads = Advertisement.objects.all()
#     return render(request, 'dashboard.html', {
#         'players': players,
#         'games': games,
#         'ads': ads
#     })
