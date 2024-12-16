from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from task_manager.mixins.forms import FormWidgetMixin


class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        fields = UserCreationForm.Meta.fields + ('first_name', 'last_name')


class UserUpdateForm(FormWidgetMixin, forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name']
