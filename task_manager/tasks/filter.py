import django_filters
from django import forms
from .models import Task
from task_manager.labels.models import Label
from task_manager.statuses.models import Status
from django.contrib.auth.models import User


class TaskFilter(django_filters.FilterSet):
    status = django_filters.ModelChoiceFilter(
        queryset=Status.objects.all(),
        widget=forms.Select(attrs={'class': 'form-control'}),
        label="Статус"
    )
    executor = django_filters.ModelChoiceFilter(
        queryset=User.objects.all(),
        widget=forms.Select(attrs={'class': 'form-control'}),
        label="Исполнитель"
    )
    labels = django_filters.ModelChoiceFilter(
        queryset=Label.objects.all(),
        widget=forms.Select(attrs={'class': 'form-control'}),
        label="Метка"
    )
    self_tasks = django_filters.BooleanFilter(
        method='filter_self_tasks',
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        label="Только мои задачи"
    )

    class Meta:
        model = Task
        fields = ['status', 'executor', 'labels', 'self_tasks']

    def filter_self_tasks(self, queryset, name, value):
        if value:
            return queryset.filter(author=self.request.user)
        return queryset
