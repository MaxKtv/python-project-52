from django.urls import reverse_lazy
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.forms import PasswordChangeForm
from task_manager.mixins import ListView, CreateView, UpdateView, DeleteView
from task_manager.mixins.auth import (UserPermissionMixin,
                                      LoginMixin,
                                      LogoutMixin)
from .forms import CustomUserCreationForm, UserUpdateForm


class CustomLoginView(LoginMixin, LoginView):
    """Представление для входа пользователя"""
    template_name = 'users/login.html'
    redirect_authenticated_user = True


class CustomLogoutView(LogoutMixin, LogoutView):
    """Представление для выхода пользователя"""
    next_page = 'home'


class UserListView(ListView):
    """Представление для просмотра списка пользователей"""
    model = User
    template_name = 'users/user_list.html'


class UserCreateView(CreateView):
    """Представление для создания пользователя"""
    model = User
    form_class = CustomUserCreationForm
    template_name = 'users/register.html'
    success_url = reverse_lazy('login')
    success_message = _("User successfully registered")

    def get_success_url(self):
        return self.success_url


class UserUpdateView(UserPermissionMixin, UpdateView):
    """Представление для обновления пользователя"""
    model = User
    form_class = UserUpdateForm
    template_name = 'users/user_form.html'
    success_url = reverse_lazy('users:list')
    success_message = _("User successfully updated")
    permission_url = reverse_lazy('users:list')

    def get_context_data(self, **kwargs):
        """Добавляем форму для изменения пароля в контекст"""
        context = super().get_context_data(**kwargs)
        context['password_form'] = PasswordChangeForm(user=self.request.user)
        return context

    def post(self, request, *args, **kwargs):
        user = self.get_object()
        password_form = PasswordChangeForm(user=user, data=request.POST)

        if 'password' in request.POST and password_form.is_valid():
            password_form.save()
            update_session_auth_hash(request, password_form.user)
            return self.form_valid(self.get_form())

        if 'password' not in request.POST:
            return super().post(request, *args, **kwargs)

        return self.form_invalid(self.get_form())

class UserDeleteView(UserPermissionMixin, DeleteView):
    """Представление для удаления пользователя"""
    model = User
    template_name = 'users/user_confirm_delete.html'
    success_url = reverse_lazy('users:list')
    success_message = _("User successfully deleted")
    protected_url = reverse_lazy('users:list')
    permission_url = reverse_lazy('users:list')
    protected_message = _("You don't have rights to delete "
                          "this user because its in use")
