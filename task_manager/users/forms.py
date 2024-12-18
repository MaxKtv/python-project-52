from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from task_manager.mixins.forms import FormWidgetMixin
from django.utils.translation import gettext_lazy as _


class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        fields = UserCreationForm.Meta.fields + ('first_name', 'last_name')
        labels = {
            "username": _("Username"),
        }


class CustomUserUpdateForm(UserChangeForm):
    """Форма для обновления данных пользователя и изменения пароля"""

    password = None  # Убираем поле, связанное с паролем

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']

    def clean_password(self):
        # Убеждаемся, что поле пароля полностью исключено
        return ""


class UserUpdateForm(UserChangeForm):
    """Форма для изменения данных пользователя и пароля"""

    password = None  # Убираем стандартное поле пароля

    password1 = forms.CharField(
        label=_("New Password"),
        required=False,
        widget=forms.PasswordInput,
    )
    password2 = forms.CharField(
        label=_("Confirm New Password"),
        required=False,
        widget=forms.PasswordInput,
    )

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name']

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get('password1')
        password2 = cleaned_data.get('password2')

        if password1 or password2:
            if password1 != password2:
                raise forms.ValidationError(_("Passwords do not match."))

        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        password1 = self.cleaned_data.get('password1')

        if password1:
            user.set_password(password1)
        if commit:
            user.save()
        return user