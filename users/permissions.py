from rest_framework import permissions


class IsLibrarianPermission(permissions.BasePermission):
    """
    Проверка наличия у пользователя группы librarian.
    """

    def has_permission(self, request, view):
        return request.user.groups.filter(name="librarian").exists()
