from rest_framework import permissions
from reviews.models import CustomUser

class AuthorAdminModeratorOrReadOnly(permissions.BasePermission):

    def has_permission(self, request, view):
        return (
            request.method in permissions.SAFE_METHODS
            or request.user.is_authenticated
        )

    def has_object_permission(self, request, view, obj):
        return (
            request.method in permissions.SAFE_METHODS
            or obj.author == request.user
            or request.user.role == CustomUser.ADMIN
            or request.user.role ==CustomUser.MODERATOR
        )

class IsAdmin(permissions.BasePermission):

    message = 'У вас недостаточно прав!'

    def has_permission(self, request, view):
        return request.user.is_authenticated and (
            request.user.is_admin or request.user.is_superuser)


class IsAdminOrReadOnly(permissions.BasePermission):

    message = 'Возможно но не сейчас)'

    def has_permission(self, request, view):
        return (request.method in permissions.SAFE_METHODS
                or (request.user.is_authenticated and (
                    request.user.is_admin or request.user.is_superuser)))

