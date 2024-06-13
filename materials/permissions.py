from rest_framework.permissions import BasePermission

class IsModerator(BasePermission):
    def has_permission(self, request, view):
        if request.user.is_staff:
            return True
        return "Отказано в доступе"

class IsNotModerator(BasePermission):
    def has_object_permission(self, request, view, obj):
        if obj.owner == request.user or request.user.is_superuser:
            return True
        return "Отказано в доступе"

class IsAuth(BasePermission):
    def has_permission(self, request, view):
        if request.user == view.get_object().owner:
            return True
        return "Отказано в доступе"