from django import forms
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _

from task_manager.labels.models import Label
from task_manager.mixins.forms import FormWidgetMixin, BaseNameModelForm
from task_manager.statuses.models import Status
from .models import Task


class TaskForm(FormWidgetMixin, BaseNameModelForm):
    description = forms.CharField(
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        label=_("Description")
    )

    status = forms.ModelChoiceField(
        queryset=Status.objects.all(),
        widget=FormWidgetMixin.get_form_widget(),
        label=_("Status")
    )

    executor = forms.ModelChoiceField(
        queryset=User.objects.all(),
        widget=FormWidgetMixin.get_form_widget(),
        required=False,
        label=_("Executor")
    )

    labels = forms.ModelMultipleChoiceField(
        queryset=Label.objects.all(),
        widget=forms.SelectMultiple(attrs={'class': 'form-select'}),
        required=False,
        label=_("Labels")
    )

    class Meta:
        model = Task
        fields = ['name', 'description', 'status', 'executor', 'labels']
