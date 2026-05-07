"""
Views для API объявлений.
"""

from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated, AllowAny

from advertisements.filters import AdvertisementFilter
from advertisements.models import Advertisement
from advertisements.permissions import IsOwnerOrReadOnly
from advertisements.serializers import AdvertisementSerializer


class AdvertisementViewSet(viewsets.ModelViewSet):
    """
    ViewSet для работы с объявлениями.
    
    Поддерживает все CRUD операции:
    - list: просмотр списка объявлений (доступно всем)
    - retrieve: просмотр одного объявления (доступно всем)
    - create: создание объявления (только авторизованным)
    - update: обновление объявления (только создателю)
    - partial_update: частичное обновление (только создателю)
    - destroy: удаление объявления (только создателю)
    
    Фильтрация:
    - По дате создания (created_at_after, created_at_before)
    - По статусу (status)
    
    Throttling:
    - Неавторизованные: 10 запросов/минуту
    - Авторизованные: 20 запросов/минуту
    """
    
    queryset = Advertisement.objects.all()
    serializer_class = AdvertisementSerializer
    filterset_class = AdvertisementFilter
    
    def get_permissions(self):
        """
        Определяет права доступа в зависимости от действия.
        
        - list, retrieve: доступно всем (AllowAny)
        - create: только авторизованным (IsAuthenticated)
        - update, partial_update, destroy: только создателю (IsOwnerOrReadOnly)
        
        Returns:
            list: Список объектов прав доступа
        """
        if self.action in ["list", "retrieve"]:
            permission_classes = [AllowAny]
        elif self.action == "create":
            permission_classes = [IsAuthenticated]
        else:  # update, partial_update, destroy
            permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]
        
        return [permission() for permission in permission_classes]
