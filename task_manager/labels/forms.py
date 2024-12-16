from .models import Label
from task_manager.mixins.forms import BaseNameModelForm


class LabelForm(BaseNameModelForm):
    class Meta:
        model = Label
        fields = ['name']
