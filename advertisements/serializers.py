"""
Сериализаторы для API объявлений.
"""

from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from advertisements.models import Advertisement, AdvertisementStatusChoices


class UserSerializer(serializers.ModelSerializer):
    """Сериализатор для модели User."""
    
    class Meta:
        model = User
        fields = ["id", "username", "first_name", "last_name"]


class AdvertisementSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Advertisement."""
    
    creator = UserSerializer(read_only=True)
    
    class Meta:
        model = Advertisement
        fields = [
            "id",
            "title",
            "description",
            "creator",
            "status",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["creator", "created_at", "updated_at"]
    
    def validate(self, data):
        """
        Валидация данных объявления.
        
        Проверяет, что у пользователя не больше 10 открытых объявлений.
        """
        # Получаем пользователя из контекста
        user = self.context["request"].user
        
        # Проверяем только при создании или изменении статуса на OPEN
        is_creating = self.instance is None
        status = data.get("status", AdvertisementStatusChoices.OPEN)
        
        # Если создаём новое объявление или меняем статус на OPEN
        if (is_creating and status == AdvertisementStatusChoices.OPEN) or \
           (not is_creating and 
            status == AdvertisementStatusChoices.OPEN and 
            self.instance.status != AdvertisementStatusChoices.OPEN):
            
            # Подсчитываем открытые объявления пользователя
            open_count = Advertisement.objects.filter(
                creator=user,
                status=AdvertisementStatusChoices.OPEN
            ).count()
            
            if open_count >= 10:
                raise ValidationError(
                    "У вас уже есть 10 открытых объявлений. "
                    "Закройте некоторые из них перед созданием новых."
                )
        
        return data
    
    def create(self, validated_data):
        """Создание объявления с автоматической установкой создателя."""
        validated_data["creator"] = self.context["request"].user
        return super().create(validated_data)
