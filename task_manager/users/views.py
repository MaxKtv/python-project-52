from django.urls import reverse_lazy
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _
from task_manager.mixins import ListView, CreateView, UpdateView, DeleteView
from task_manager.mixins.auth import UserPermissionMixin
from .forms import CustomUserCreationForm, UserUpdateForm


# Общие сообщения
PERMISSION_DENIED_MESSAGE = _("You don't have rights to modify another user")


class UserListView(ListView):
    """Представление для просмотра списка пользователей"""
    model = User
    template_name = 'users/user_list.html'


class UserCreateView(CreateView):
    """Представление для регистрации пользователя"""
    model = User
    form_class = CustomUserCreationForm
    template_name = 'users/register.html'
    success_url = reverse_lazy('login')
    success_message = _("User successfully registered")


class UserUpdateView(UserPermissionMixin, UpdateView):
    """Представление для обновления пользователя"""
    model = User
    form_class = UserUpdateForm
    template_name = 'users/user_form.html'
    success_url = reverse_lazy('users:list')
    success_message = _("User successfully updated")
    permission_message = PERMISSION_DENIED_MESSAGE


class UserDeleteView(UserPermissionMixin, DeleteView):
    """Представление для удаления пользователя"""
    model = User
    template_name = 'users/user_confirm_delete.html'
    success_url = reverse_lazy('users:list')
    success_message = _("User successfully deleted")
    permission_message = PERMISSION_DENIED_MESSAGE
