import django_filters
from django import forms
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _

from task_manager.labels.models import Label
from task_manager.statuses.models import Status

from .models import Task


class TaskFilter(django_filters.FilterSet):
    """Фильтр для задач"""

    request = None  # Добавляем атрибут класса

    status = django_filters.ModelChoiceFilter(
        queryset=Status.objects.all(),
        label=_("Status"),
        empty_label="---------",
    )

    executor = django_filters.ModelChoiceFilter(
        queryset=get_user_model().objects.all(),
        label=_("Executor"),
        empty_label="---------",
    )

    labels = django_filters.ModelChoiceFilter(
        queryset=Label.objects.all(),
        label=_("Label"),
        empty_label="---------",
    )

    self_tasks = django_filters.BooleanFilter(
        label=_("Only my tasks"),
        method="filter_self_tasks",
        widget=forms.CheckboxInput(
            attrs={"class": "form-check-input", "role": "switch"}
        ),
    )

    def filter_self_tasks(self, queryset, name, value):
        """Фильтрует задачи по текущему пользователю как автору"""
        if value:
            user = self.request.user
            return queryset.filter(author=user)
        return queryset

    class Meta:
        model = Task
        fields = ["status", "executor", "labels", "self_tasks"]
        order_by = ["id"]
