"""
Конфигурация приложения advertisements.
"""

from django.apps import AppConfig


class AdvertisementsConfig(AppConfig):
    """Конфигурация приложения для управления объявлениями."""
    
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'advertisements'
    verbose_name = 'Объявления'
