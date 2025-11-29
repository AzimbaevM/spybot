from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('api.urls')),       # DRF API для игроков, игр, рекламы
    # path('panel/', include('gamepanel.urls')),  # Веб-панель (если нужна)
]
