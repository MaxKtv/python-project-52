from task_manager.base import BaseNameModelForm

from .models import Label


class LabelForm(BaseNameModelForm):
    class Meta:
        model = Label
        fields = ["name"]
