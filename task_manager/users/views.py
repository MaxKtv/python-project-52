from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.views.generic.list import ListView

from task_manager.mixins import ProtectedMessageMixin, UserPermissionMixin

from .forms import CustomUserCreationForm, UserUpdateForm


class CustomLoginView(LoginView):
    """Представление для входа пользователя"""

    template_name = "users/login.html"
    redirect_authenticated_user = True

    def form_valid(self, form):
        messages.success(self.request, _("You are logged in"))
        return super().form_valid(form)


class CustomLogoutView(LogoutView):
    """Представление для выхода пользователя"""

    next_page = "home"

    def dispatch(self, request, *args, **kwargs):
        messages.info(self.request, _("You are logged out"))
        return super().dispatch(request, *args, **kwargs)


class UserListView(ListView):
    """Представление для просмотра списка пользователей"""

    model = User
    template_name = "users/user_list.html"
    ordering = ['id']


class UserCreateView(SuccessMessageMixin, CreateView):
    """Представление для создания пользователя"""

    model = User
    form_class = CustomUserCreationForm
    template_name = "users/register.html"
    success_url = reverse_lazy("login")
    success_message = _("User successfully registered")


class UserUpdateView(UserPermissionMixin, SuccessMessageMixin, UpdateView):
    """Представление для обновления пользователя"""

    model = User
    form_class = UserUpdateForm
    template_name = "users/user_form.html"
    success_url = reverse_lazy("users:list")
    success_message = _("User successfully updated")
    permission_url = reverse_lazy("users:list")


class UserDeleteView(UserPermissionMixin, ProtectedMessageMixin, DeleteView):
    """Представление для удаления пользователя"""

    model = User
    template_name = "users/user_confirm_delete.html"
    success_url = reverse_lazy("users:list")
    success_message = _("User successfully deleted")
    protected_url = reverse_lazy("users:list")
    permission_url = reverse_lazy("users:list")
    protected_message = _(
        "You don't have rights to delete this user because its in use"
    )
