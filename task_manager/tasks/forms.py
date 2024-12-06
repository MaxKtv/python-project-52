from django import forms
from .models import Task
from task_manager.labels.models import Label
from django.utils.translation import gettext_lazy as _


class TaskForm(forms.ModelForm):
    labels = forms.ModelMultipleChoiceField(
        queryset=Label.objects.all(),
        widget=forms.SelectMultiple(attrs={'class': 'form-control'}),
        required=False,
        label=_("Labels")
    )

    class Meta:
        model = Task
        fields = ['name', 'description', 'status', 'executor', 'labels']
