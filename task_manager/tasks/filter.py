import django_filters
from django import forms
from django.contrib.auth.models import User
from .models import Task
from task_manager.statuses.models import Status
from task_manager.labels.models import Label
from task_manager.mixins import CustomFormWidgetMixin


class TaskFilter(django_filters.FilterSet, CustomFormWidgetMixin):
    executor = django_filters.ModelChoiceFilter(
        queryset=User.objects.all(),
        widget=CustomFormWidgetMixin.get_form_widget(User.objects.all())
    )

    status = django_filters.ModelChoiceFilter(
        queryset=Status.objects.all(),
        widget=CustomFormWidgetMixin.get_form_widget(Status.objects.all())
    )

    labels = django_filters.ModelChoiceFilter(
        queryset=Label.objects.all(),
        widget=CustomFormWidgetMixin.get_form_widget(Label.objects.all())
    )

    self_tasks = django_filters.BooleanFilter(
        widget=forms.CheckboxInput,
        method='filter_self_tasks',
        label='Только свои задачи'
    )

    def filter_self_tasks(self, queryset, name, value):
        if value:
            return queryset.filter(author=self.request.user)
        return queryset

    class Meta:
        model = Task
        fields = ['status', 'executor', 'labels', 'self_tasks']
