from django.urls import reverse_lazy
from django.views.generic import ListView
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from task_manager.mixins import (
    CustomCreateView, CustomUpdateView, CustomPermissionMixin, CustomDeleteMixin
)
from django.contrib import messages
from django.shortcuts import redirect
from django.utils.translation import gettext_lazy as _


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
    ordering = ['id']


class UserCreateView(CustomCreateView):
    model = User
    form_class = CustomUserCreationForm
    template_name = 'users/register.html'
    success_url = reverse_lazy('login')
    success_message = _("User successfully registered")


class UserUpdateView(CustomUpdateView, CustomPermissionMixin):
    model = User
    fields = ['username', 'first_name', 'last_name']
    template_name = 'users/user_form.html'
    success_url = reverse_lazy('user_list')
    success_message = _("User successfully updated")
    permission_message = _("You don't have rights to modify the user")
    permission_url = 'user_list'

    def test_func(self):
        return self.request.user.is_superuser


class UserDeleteView(CustomPermissionMixin, CustomDeleteMixin):
    model = User
    template_name = 'users/user_confirm_delete.html'
    success_url = reverse_lazy('user_list')
    success_message = _("User successfully deleted")
    permission_message = _("You don't have rights to delete the user")
    permission_url = 'user_list'

    def dispatch(self, request, *args, **kwargs):
        user = self.get_object()
        if not (request.user.is_superuser or request.user.id == user.id):
            messages.error(
                request,
                self.permission_message,
                extra_tags='danger'
            )
            return redirect(self.permission_url)
        return super().dispatch(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        if self.get_object().task_set.exists():
            messages.error(
                request,
                _("Cannot delete user because they have associated tasks"),
                extra_tags='danger'
            )
            return redirect('user_list')
        return super().delete(request, *args, **kwargs)
