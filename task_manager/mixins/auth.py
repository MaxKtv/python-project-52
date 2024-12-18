from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib import messages
from django.shortcuts import redirect
from django.utils.translation import gettext_lazy as _
from django.urls import reverse_lazy


class BaseAuthMixin:
    """Базовый миксин для обработки аутентификации и ошибок доступа."""
    permission_message = _("You are not authorized! Please log in.")
    permission_url = reverse_lazy('login')

    def get_login_url(self):
        return getattr(self, 'login_url', reverse_lazy('login'))

    def get_permission_url(self):
        return getattr(self, 'permission_url', reverse_lazy('login'))

    def redirect_with_error(self, error_message, url):
        messages.error(self.request, error_message)
        if not url:
            url = reverse_lazy('login')
        return redirect(url)

    def handle_no_permission(self):
        """Обработка случаев отсутствия разрешений."""
        if not self.request.user.is_authenticated:
            return self.redirect_with_error(
                _("You are not authorized! Please log in."),
                self.get_login_url()
            )
        return self.redirect_with_error(
            self.permission_message, self.get_permission_url()
        )


class AuthRequiredMixin(LoginRequiredMixin, BaseAuthMixin):
    """Миксин для страниц, требующих аутентификации."""
    login_url = reverse_lazy('login')


class AuthMixin(BaseAuthMixin):
    """Миксин для аутентификации только для POST-запросов."""
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated and request.method != 'GET':
            return self.handle_no_permission()
        return super().dispatch(request, *args, **kwargs)


class BasePermissionMixin(BaseAuthMixin, UserPassesTestMixin):
    """Базовый миксин для проверки прав."""
    permission_message = _("You don't have sufficient permissions.")

    def handle_no_permission(self):
        """Обработка случаев отсутствия разрешений"""
        if not self.request.user.is_authenticated:
            return self.redirect_with_error(
                _("You are not authorized! Please log in."),
                self.get_login_url()
            )
        return self.redirect_with_error(
            self.permission_message, self.get_permission_url()
        )


class UserPermissionMixin(BasePermissionMixin):
    """Миксин для проверки прав на управление пользователями."""
    permission_message = _("You don't have permissions to modify user")
    permission_url = reverse_lazy('users:list')

    def test_func(self):
        user = self.get_object()
        return self.request.user == user


class SuperuserRequiredMixin(BasePermissionMixin):
    """Миксин для проверки прав администратора."""
    permission_message = _("Only superusers can do this.")
    permission_url = reverse_lazy('home')

    def test_func(self):
        return self.request.user.is_superuser


class TaskAuthorRequiredMixin(BasePermissionMixin):
    """Миксин для проверки, является ли пользователь автором задачи."""
    permission_message = _("A task can only be deleted by its author")
    permission_url = reverse_lazy('tasks:list')

    def test_func(self):
        task = self.get_object()
        return task.author == self.request.user


class LoginMixin:
    """Миксин для добавления сообщения об успешном входе."""
    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, _("You are logged in"))
        return response


class LogoutMixin:
    """Миксин для добавления сообщения о выходе."""
    def dispatch(self, request, *args, **kwargs):
        messages.info(request, _("You are logged out"))
        return super().dispatch(request, *args, **kwargs)
