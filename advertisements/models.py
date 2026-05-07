"""
Модели для приложения advertisements.
"""

from django.contrib.auth.models import User
from django.db import models


class AdvertisementStatusChoices(models.TextChoices):
    """Статусы объявления."""
    
    OPEN = "OPEN", "Открыто"
    CLOSED = "CLOSED", "Закрыто"


class Advertisement(models.Model):
    """Модель объявления."""
    
    title = models.CharField(
        max_length=200,
        verbose_name="Заголовок",
        help_text="Краткий заголовок объявления"
    )
    
    description = models.TextField(
        verbose_name="Описание",
        help_text="Подробное описание объявления"
    )
    
    creator = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="advertisements",
        verbose_name="Создатель",
        help_text="Пользователь, создавший объявление"
    )
    
    status = models.CharField(
        max_length=10,
        choices=AdvertisementStatusChoices.choices,
        default=AdvertisementStatusChoices.OPEN,
        verbose_name="Статус",
        help_text="Текущий статус объявления"
    )
    
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Дата создания",
        db_index=True
    )
    
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name="Дата обновления"
    )
    
    class Meta:
        verbose_name = "Объявление"
        verbose_name_plural = "Объявления"
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["-created_at"]),
            models.Index(fields=["status"]),
        ]
    
    def __str__(self) -> str:
        """Строковое представление объявления."""
        return f"{self.title} ({self.get_status_display()})"
