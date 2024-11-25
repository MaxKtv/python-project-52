from django.db import models
from django.contrib.auth.models import User
from task_manager.statuses.models import Status  # Импорт модели статуса
from django.urls import reverse
from task_manager.labels.models import Label


class Task(models.Model):
    name = models.CharField(max_length=100, verbose_name="Имя задачи")
    description = models.TextField(blank=True, verbose_name="Описание")
    status = models.ForeignKey(Status, on_delete=models.PROTECT, verbose_name="Статус")
    author = models.ForeignKey(User, on_delete=models.PROTECT, related_name='authored_tasks', verbose_name="Автор")
    executor = models.ForeignKey(User, on_delete=models.SET_NULL, related_name='assigned_tasks', null=True, blank=True, verbose_name="Исполнитель")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    labels = models.ManyToManyField(Label, blank=True, verbose_name="Метки")

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('task_detail', args=[str(self.id)])
