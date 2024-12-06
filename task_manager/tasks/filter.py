import django_filters
from django import forms
from django.contrib.auth.models import User
from .models import Task
from task_manager.statuses.models import Status
from task_manager.labels.models import Label
from task_manager.mixins import CustomFormWidgetMixin
from django.utils.translation import gettext_lazy as _


class BaseModelChoiceFilter:
    @staticmethod
    def create_filter(model_class):
        return django_filters.ModelChoiceFilter(
            queryset=model_class.objects.all(),
            widget=CustomFormWidgetMixin.get_form_widget
            (model_class.objects.all())
        )


class TaskFilter(django_filters.FilterSet, CustomFormWidgetMixin):
    executor = BaseModelChoiceFilter.create_filter(User)
    status = BaseModelChoiceFilter.create_filter(Status)
    labels = BaseModelChoiceFilter.create_filter(Label)

    self_tasks = django_filters.BooleanFilter(
        widget=forms.CheckboxInput,
        method='filter_self_tasks',
        label=_('Only my tasks')
    )

    def filter_self_tasks(self, queryset, name, value):
        if value:
            return queryset.filter(author=self.request.user)
        return queryset

    class Meta:
        model = Task
        fields = ['status', 'executor', 'labels', 'self_tasks']
