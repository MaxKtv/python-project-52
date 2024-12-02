from django.urls import reverse_lazy
from django.views.generic import ListView
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from task_manager.mixins import (
    CustomCreateView, CustomUpdateView, CustomPermissionMixin, CustomDeleteMixin
)
from django.contrib import messages
from django.shortcuts import redirect


class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        fields = UserCreationForm.Meta.fields + ('first_name', 'last_name')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'


class UserListView(ListView):
    model = User
    template_name = 'users/user_list.html'


class UserCreateView(CustomCreateView):
    model = User
    form_class = CustomUserCreationForm
    template_name = 'users/register.html'
    success_url = reverse_lazy('login')
    success_message = "Пользователь успешно зарегистрирован"


class UserUpdateView(CustomUpdateView, CustomPermissionMixin):
    model = User
    fields = ['username', 'first_name', 'last_name']
    template_name = 'users/user_form.html'
    success_url = reverse_lazy('user_list')
    success_message = "Пользователь успешно изменён"
    permission_message = "У вас нет прав для изменения пользователя"
    permission_url = 'user_list'

    def test_func(self):
        return self.request.user.is_superuser


class UserDeleteView(CustomPermissionMixin, CustomDeleteMixin):
    model = User
    template_name = 'users/user_confirm_delete.html'
    success_url = reverse_lazy('user_list')
    success_message = "Пользователь успешно удалён"
    permission_message = "У вас нет прав для удаления пользователя"
    permission_url = 'user_list'

    def test_func(self):
        return (self.request.user.is_superuser
                or self.request.user.id == self.get_object().id)

    def delete(self, request, *args, **kwargs):
        if self.get_object().task_set.exists():
            messages.error(
                request,
                "Невозможно удалить пользователя, потому что он используется",
                extra_tags='danger'
            )
            return redirect('user_list')
        return super().delete(request, *args, **kwargs)
