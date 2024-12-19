from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

from task_manager.base import NamedModel
from task_manager.labels.models import Label
from task_manager.statuses.models import Status


class Task(NamedModel):
    description = models.TextField(blank=True, verbose_name=_("Description"))

    status = models.ForeignKey(
        Status, on_delete=models.PROTECT, verbose_name=_("Status")
    )

    author = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        related_name="authored_tasks",
        verbose_name=_("Author"),
    )

    executor = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        related_name="assigned_tasks",
        null=True,
        blank=True,
        verbose_name=_("Executor"),
    )

    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name=_("Created at")
    )

    labels = models.ManyToManyField(Label, blank=True, verbose_name=_("Labels"))

    def get_absolute_url(self):
        return reverse("task_detail", args=[str(self.id)])
