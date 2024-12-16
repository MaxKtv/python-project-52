from django.utils.translation import gettext_lazy as _
from django import forms
from django.forms import Select


# Общие атрибуты виджетов
FORM_CONTROL_ATTRS = {'class': 'form-control'}


class FormWidgetMixin:
    """Миксин для получения виджета формы"""
    @staticmethod
    def get_form_widget(queryset=None):
        """Возвращает виджет формы"""
        widget = Select(attrs=FORM_CONTROL_ATTRS)
        if queryset:
            widget.choices = [(obj.pk, str(obj)) for obj in queryset]
        return widget


class BaseNameModelForm(forms.ModelForm):
    """Базовый класс формы для моделей с полем name"""
    name = forms.CharField(
        label=_('Name'),
        widget=forms.TextInput(attrs=FORM_CONTROL_ATTRS)
    )
