from django.utils.translation import gettext_lazy as _
from task_manager.mixins.base import NamedModel


class Label(NamedModel):
    class Meta(NamedModel.Meta):
        verbose_name = _('Label')
        verbose_name_plural = _('Labels')
