from rest_framework import permissions


class AuthorAdminModeratorOrReadOnly(permissions.BasePermission):
    """ Вносить изменения могут автор, админ, модератор"""
    def has_permission(self, request, view):
        return (
            request.method in permissions.SAFE_METHODS
            or request.user.is_authenticated
        )

    def has_object_permission(self, request, view, obj):
        return (
            request.method in permissions.SAFE_METHODS
            or request.user.is_admin
            or request.user.is_moderator
            or obj.author == request.user
        )


class IsAdmin(permissions.BasePermission):
    """ Видимость только для администратора"""
    message = 'У вас недостаточно прав!'

    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_admin


class IsAdminOrReadOnly(permissions.BasePermission):
    """ Доступ для внесения изменений только для администратора. """
    message = 'Возможно но не сейчас)'

    def has_permission(self, request, view):
        return (request.method in permissions.SAFE_METHODS
                or (request.user.is_authenticated and request.user.is_admin))
