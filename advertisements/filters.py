"""
Фильтры для API объявлений.
"""

from django_filters import rest_framework as filters

from advertisements.models import Advertisement


class AdvertisementFilter(filters.FilterSet):
    """
    Фильтр для объявлений.
    
    Поддерживает фильтрацию по:
    - created_at: диапазон дат создания
    - status: статус объявления
    """
    
    created_at = filters.DateFromToRangeFilter(
        field_name="created_at",
        label="Дата создания (от-до)"
    )
    
    class Meta:
        model = Advertisement
        fields = ["created_at", "status"]
