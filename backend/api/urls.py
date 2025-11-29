from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PlayerViewSet, GameViewSet, GamePlayerViewSet, AdvertisementViewSet

router = DefaultRouter()
router.register(r'players', PlayerViewSet)
router.register(r'games', GameViewSet)
router.register(r'gameplayers', GamePlayerViewSet)
router.register(r'advertisements', AdvertisementViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
