"""
Кастомные права доступа для API объявлений.
"""

from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsOwnerOrReadOnly(BasePermission):
    """
    Право доступа, позволяющее только владельцу изменять объект.
    
    Любой пользователь может читать объекты (GET, HEAD, OPTIONS),
    но изменять (PUT, PATCH, DELETE) может только создатель объявления.
    """
    
    def has_object_permission(self, request, view, obj):
        """
        Проверка прав доступа к конкретному объекту.
        
        Args:
            request: HTTP запрос
            view: View, обрабатывающий запрос
            obj: Объект, к которому запрашивается доступ
            
        Returns:
            bool: True, если доступ разрешён
        """
        # Чтение разрешено всем
        if request.method in SAFE_METHODS:
            return True
        
        # Изменение разрешено только создателю
        return obj.creator == request.user
