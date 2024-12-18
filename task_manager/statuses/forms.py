from task_manager.mixins.forms import BaseNameModelForm

from .models import Status


class StatusForm(BaseNameModelForm):
    class Meta:
        model = Status
        fields = ['name']
