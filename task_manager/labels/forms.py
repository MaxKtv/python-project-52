from task_manager.mixins.forms import BaseNameModelForm
from .models import Label


class LabelForm(BaseNameModelForm):
    class Meta:
        model = Label
        fields = ['name']
