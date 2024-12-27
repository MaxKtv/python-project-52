from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.db.models import ProtectedError
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _

NOT_AUTHORIZED_MESSAGE = _("You are not authorized! Please log in.")
NOT_PERMISSION_MODIFY_USER = _("You don't have permissions to modify user")
NOT_TASKS_AUTHOR = _("A task can only be deleted by its author")


class AuthRequiredMixin(LoginRequiredMixin):
    """Миксин для проверки аутентификации."""
    auth_message = NOT_AUTHORIZED_MESSAGE

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.error(request, self.auth_message)
            return redirect(reverse_lazy('login'))

        return super().dispatch(request, *args, **kwargs)


class UserPermissionMixin(AuthRequiredMixin, UserPassesTestMixin):
    """Миксин для проверки прав на управление пользователями."""
    permission_message = NOT_PERMISSION_MODIFY_USER
    permission_url = reverse_lazy('users:list')

    def test_func(self):
        user = self.get_object()
        return self.request.user == user

    def handle_no_permission(self):
        messages.error(self.request, self.permission_message)
        return redirect(self.permission_url)


class AuthorPermissionMixin(UserPassesTestMixin):
    """Миксин для проверки, является ли пользователь автором задачи."""
    permission_message = NOT_TASKS_AUTHOR
    permission_url = reverse_lazy('tasks:list')

    def test_func(self):
        task = self.get_object()
        return task.author == self.request.user

    def handle_no_permission(self):
        messages.error(self.request, self.permission_message)
        return redirect(self.permission_url)


class ProtectedMessageMixin:
    """
    Миксин для отображения сообщения, если объект
    защищен от удаления или действия.
    """
    protected_message = _(
        "Cannot delete this object because " "it's referenced by other objects."
    )
    success_message = _("Object deleted successfully.")
    success_url = reverse_lazy("home")

    def handle_protected_error(self):
        messages.error(self.request, self.protected_message)
        return redirect(self.success_url)

    def post(self, request, *args, **kwargs):
        try:
            response = super().post(request, *args, **kwargs)
            messages.success(request, self.success_message)
            return response
        except ProtectedError:
            return self.handle_protected_error()
