from django.contrib import messages
from django.contrib.auth.mixins import UserPassesTestMixin
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _

NOT_AUTHORIZED_MESSAGE = _("You are not authorized! Please log in.")


class BaseAuth:
    """Базовый класс для обработки аутентификации и ошибок доступа."""

    permission_message = NOT_AUTHORIZED_MESSAGE
    permission_url = reverse_lazy("login")

    def get_login_url(self):
        return getattr(self, "login_url", reverse_lazy("login"))

    def get_permission_url(self):
        return getattr(self, "permission_url", reverse_lazy("login"))

    def redirect_with_error(self, error_message, url):
        messages.error(self.request, error_message)
        if not url:
            url = reverse_lazy("login")
        return redirect(url)

    def handle_no_permission(self):
        """Обработка случаев отсутствия разрешений."""
        if not self.request.user.is_authenticated:
            return self.redirect_with_error(
                NOT_AUTHORIZED_MESSAGE, self.get_login_url(),
            )
        return self.redirect_with_error(
            self.permission_message, self.get_permission_url()
        )


class BasePermissionMixin(BaseAuth, UserPassesTestMixin):
    """Базовый миксин для проверки прав."""
    def test_func(self):
        pass


class AuthPermissionMixin(BasePermissionMixin):
    """Миксин для проверки аутентификации."""
    def test_func(self):
        return self.request.user.is_authenticated


class UserPermissionMixin(BasePermissionMixin):
    """Миксин для проверки прав на управление пользователями."""

    permission_message = _("You don't have permissions to modify user")
    permission_url = reverse_lazy("users:list")

    def test_func(self):
        user = self.get_object()
        return self.request.user == user


class AuthorPermissionMixin(BasePermissionMixin):
    """Миксин для проверки, является ли пользователь автором задачи."""

    permission_message = _("A task can only be deleted by its author")
    permission_url = reverse_lazy("tasks:list")

    def test_func(self):
        task = self.get_object()
        return task.author == self.request.user
