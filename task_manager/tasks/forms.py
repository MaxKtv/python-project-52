from django import forms
from .models import Task
from task_manager.labels.models import Label


class TaskForm(forms.ModelForm):
    labels = forms.ModelMultipleChoiceField(
        queryset=Label.objects.all(),
        widget=forms.SelectMultiple(attrs={'class': 'form-control'}),
        required=False,
        label="Метки"
    )

    class Meta:
        model = Task
        fields = ['name', 'description', 'status', 'executor', 'labels']
