from task_manager.base import BaseNameModelForm

from .models import Status


class StatusForm(BaseNameModelForm):
    class Meta:
        model = Status
        fields = ["name"]
