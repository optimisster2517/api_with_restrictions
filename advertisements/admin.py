"""
Конфигурация Django админки для объявлений.
"""

from django.contrib import admin

from advertisements.models import Advertisement


@admin.register(Advertisement)
class AdvertisementAdmin(admin.ModelAdmin):
    """Настройки админки для модели Advertisement."""
    
    list_display = [
        "id",
        "title",
        "creator",
        "status",
        "created_at",
        "updated_at",
    ]
    
    list_filter = [
        "status",
        "created_at",
    ]
    
    search_fields = [
        "title",
        "description",
        "creator__username",
    ]
    
    readonly_fields = [
        "created_at",
        "updated_at",
    ]
    
    fieldsets = (
        ("Основная информация", {
            "fields": ("title", "description", "creator", "status")
        }),
        ("Даты", {
            "fields": ("created_at", "updated_at"),
            "classes": ("collapse",)
        }),
    )
    
    date_hierarchy = "created_at"
    
    def get_queryset(self, request):
        """Оптимизация запросов с select_related."""
        queryset = super().get_queryset(request)
        return queryset.select_related("creator")
