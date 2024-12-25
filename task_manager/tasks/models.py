from django.contrib.auth.models import User
from django.db import models
from django.utils.translation import gettext_lazy as _

from task_manager.labels.models import Label
from task_manager.statuses.models import Status

User.add_to_class(
    "__str__",
    lambda self: f"{self.first_name} "
                 f"{self.last_name}".strip()
                 or self.username
)


class Task(models.Model):
    name = models.CharField(
        max_length=30,
        unique=True,
        verbose_name=_('Name'),
    )
    description = models.CharField(
        max_length=255,
        blank=True,
        verbose_name=_('Description'),
    )
    author = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        related_name='author_tasks',
        verbose_name=_('Author'),
    )
    executor = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        related_name='executor_tasks',
        null=True,
        blank=True,
        verbose_name=_('Executor'),
    )
    status = models.ForeignKey(
        Status,
        on_delete=models.PROTECT,
        verbose_name=_('Status'),
    )
    labels = models.ManyToManyField(
        Label,
        through='TaskLabel',
        related_name='label_tasks',
        verbose_name=_('Labels'),
        blank=True,
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _('Task')


class TaskLabel(models.Model):
    """
    Промежуточная модель для связи задач (Task) и меток (Label).
    """
    task = models.ForeignKey(Task,
                             on_delete=models.CASCADE)
    label = models.ForeignKey(Label,
                              on_delete=models.PROTECT)  # Защита от удаления

    class Meta:
        unique_together = ('task', 'label')
