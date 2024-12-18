from django import forms
from django.forms import Select
from django.utils.translation import gettext_lazy as _


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

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Пример кастомизации для ModelChoiceField
        for field_name, field in self.fields.items():
            if isinstance(field, forms.ModelChoiceField):
                field.label_from_instance = self.get_label_from_instance

    def get_label_from_instance(self, obj):
        """Настраиваем отображение вариантов для ModelChoiceField"""
        if hasattr(obj, 'first_name') and hasattr(obj, 'last_name'):
            full_name = f"{obj.first_name} {obj.last_name}".strip()
            return full_name if full_name else obj.username
        return str(obj)
