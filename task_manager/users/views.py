from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _

from task_manager.base import (
    CreateView,
    DeleteView,
    ListView,
    UpdateView,
    BaseLoginView,
    BaseLogoutView,
    UserPermissionMixin,
)

from .forms import CustomUserCreationForm, UserUpdateForm


class CustomLoginView(BaseLoginView, LoginView):
    """Представление для входа пользователя"""

    template_name = "users/login.html"
    redirect_authenticated_user = True


class CustomLogoutView(BaseLogoutView, LogoutView):
    """Представление для выхода пользователя"""

    next_page = "home"


class UserListView(ListView):
    """Представление для просмотра списка пользователей"""

    model = User
    template_name = "users/user_list.html"


class UserCreateView(CreateView):
    """Представление для создания пользователя"""

    model = User
    form_class = CustomUserCreationForm
    template_name = "users/register.html"
    success_url = reverse_lazy("login")
    success_message = _("User successfully registered")

    def get_success_url(self):
        return self.success_url


class UserUpdateView(UserPermissionMixin, UpdateView):
    """Представление для обновления пользователя"""

    model = User
    form_class = UserUpdateForm
    template_name = "users/user_form.html"
    success_url = reverse_lazy("users:list")
    success_message = _("User successfully updated")
    permission_url = reverse_lazy("users:list")


class UserDeleteView(UserPermissionMixin, DeleteView):
    """Представление для удаления пользователя"""

    model = User
    template_name = "users/user_confirm_delete.html"
    success_url = reverse_lazy("users:list")
    success_message = _("User successfully deleted")
    protected_url = reverse_lazy("users:list")
    permission_url = reverse_lazy("users:list")
    protected_message = _(
        "You don't have rights to delete " "this user because its in use"
    )
