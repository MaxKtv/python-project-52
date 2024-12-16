from django.utils.translation import gettext_lazy as _
from task_manager.mixins.base import NamedModel


class Status(NamedModel):
    class Meta(NamedModel.Meta):
        verbose_name = _('Status')
        verbose_name_plural = _('Statuses')
