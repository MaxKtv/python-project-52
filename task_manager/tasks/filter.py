import django_filters
from django import forms
from django.contrib.auth import get_user_model
from .models import Task
from task_manager.statuses.models import Status
from task_manager.labels.models import Label
from django.utils.translation import gettext_lazy as _
from task_manager.mixins.forms import FormWidgetMixin


class TaskFilter(django_filters.FilterSet, FormWidgetMixin):
    """Фильтр для задач"""
    request = None  # Добавляем атрибут класса

    status = django_filters.ModelChoiceFilter(
        queryset=Status.objects.all(),
        label=_('Status'),
        empty_label='---------',
    )

    executor = django_filters.ModelChoiceFilter(
        queryset=get_user_model().objects.all(),
        label=_('Executor'),
        empty_label='---------',
    )

    labels = django_filters.ModelChoiceFilter(
        queryset=Label.objects.all(),
        label=_('Label'),
        empty_label='---------',
    )

    self_tasks = django_filters.BooleanFilter(
        label=_('Only my tasks'),
        method='filter_self_tasks',
        widget=forms.CheckboxInput(attrs={
            'class': 'form-check-input',
            'role': 'switch'
        })
    )

    def __init__(self, *args, **kwargs):
        TaskFilter.request = kwargs.pop('request', None)
        super().__init__(*args, **kwargs)

        # Устанавливаем виджеты для фильтров
        for field in ['status', 'executor', 'labels']:
            self.filters[field].widget = self.get_form_widget(
                self.filters[field].queryset
            )

    def filter_self_tasks(self, queryset, name, value):
        """Фильтрует задачи по текущему пользователю как автору"""
        if not TaskFilter.request:  # Используем атрибут класса
            return queryset
        if not hasattr(TaskFilter.request, 'user'):  # Используем атрибут класса
            return queryset
        if value and TaskFilter.request.user.is_authenticated:
            filtered = queryset.filter(author_id=TaskFilter.request.user.id)
            return filtered
        return queryset

    class Meta:
        model = Task
        fields = ['status', 'executor', 'labels', 'self_tasks']
        order_by = ['id']  # Добавляем сортировку по умолчанию
