from django.forms import ModelForm, Textarea

from .models import Task


class TaskForm(ModelForm):
    class Meta:
        model = Task
        fields = [
            'name',
            'description',
            'status',
            'executor',
            'labels'
        ]
        widgets = {
            'description': Textarea(),
        }
