from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib import messages
from django.shortcuts import redirect
from django.utils.translation import gettext_lazy as _


class BaseAuthMixin:
    """Базовый миксин для аутентификации"""
    permission_message = _("You are not authorized! Please log in.")
    permission_url = 'login'

    def handle_no_permission(self):
        messages.error(self.request, self.permission_message)
        return redirect(self.permission_url)


class AuthRequiredMixin(LoginRequiredMixin, BaseAuthMixin):
    """Миксин для страниц, требующих аутентификации"""
    pass


class AuthMixin(BaseAuthMixin):
    """Миксин для проверки аутентификации только для POST запросов"""
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated and request.method != 'GET':
            return self.handle_no_permission()
        return super().dispatch(request, *args, **kwargs)


class UserPermissionMixin(BaseAuthMixin, UserPassesTestMixin):
    """Миксин для проверки прав на управление пользователями"""
    permission_message = _("You don't have rights to modify another user")
    permission_url = 'users:list'

    def dispatch(self, request, *args, **kwargs):
        self.user_id = kwargs.get('pk')
        return super().dispatch(request, *args, **kwargs)

    def test_func(self):
        return int(self.user_id) == self.request.user.id


class SuperuserRequiredMixin(BaseAuthMixin, UserPassesTestMixin):
    """Миксин для проверки прав администратора"""
    permission_message = _("Only superusers can do this")
    permission_url = 'home'

    def test_func(self):
        return self.request.user.is_superuser


class TaskAuthorRequiredMixin(BaseAuthMixin, UserPassesTestMixin):
    """Миксин для проверки, является ли пользователь автором задачи"""
    permission_message = _("A task can only be deleted by its author")
    permission_url = 'tasks:list'

    def dispatch(self, request, *args, **kwargs):
        self.task_id = kwargs.get('pk')
        return super().dispatch(request, *args, **kwargs)

    def test_func(self):
        task = self.get_object()
        return task.author == self.request.user
