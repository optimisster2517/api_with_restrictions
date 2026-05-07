"""
URL конфигурация для приложения advertisements.
"""

from django.urls import path, include
from rest_framework.routers import DefaultRouter

from advertisements.views import AdvertisementViewSet

# Создаём роутер и регистрируем ViewSet
router = DefaultRouter()
router.register(r'advertisements', AdvertisementViewSet, basename='advertisement')

urlpatterns = [
    path('', include(router.urls)),
]
