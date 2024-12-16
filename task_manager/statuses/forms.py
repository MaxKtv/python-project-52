from .models import Status
from task_manager.mixins.forms import BaseNameModelForm


class StatusForm(BaseNameModelForm):
    class Meta:
        model = Status
        fields = ['name']
