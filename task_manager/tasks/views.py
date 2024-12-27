from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django_filters.views import FilterView

from task_manager.mixins import AuthorPermissionMixin, AuthRequiredMixin
from task_manager.tasks.models import Task

from .filter import TaskFilter
from .forms import TaskForm


class TaskListView(AuthRequiredMixin, FilterView):
    """Представление для просмотра списка задач"""

    model = Task
    filterset_class = TaskFilter
    template_name = "tasks/task_list.html"
    context_object_name = "tasks"
    ordering = ["id"]

    def get_filterset_kwargs(self, filterset_class):
        kwargs = super().get_filterset_kwargs(filterset_class)
        kwargs["request"] = self.request
        return kwargs


class TaskDetailView(AuthRequiredMixin, DetailView):
    """Представление для просмотра задачи"""

    model = Task
    template_name = "tasks/task_detail.html"


class TaskCreateView(AuthRequiredMixin, SuccessMessageMixin, CreateView):
    """Представление для создания задачи"""

    model = Task
    form_class = TaskForm
    template_name = "tasks/task_form.html"
    success_message = _("Task successfully created")
    success_url = reverse_lazy("tasks:list")

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class TaskUpdateView(AuthRequiredMixin, SuccessMessageMixin, UpdateView):
    """Представление для обновления задачи"""

    model = Task
    form_class = TaskForm
    template_name = "tasks/task_form.html"
    success_message = _("Task successfully updated")
    success_url = reverse_lazy("tasks:list")


class TaskDeleteView(AuthorPermissionMixin, SuccessMessageMixin, DeleteView):
    """Представление для удаления задачи"""

    model = Task
    template_name = "tasks/task_confirm_delete.html"
    success_message = _("Task successfully deleted")
    success_url = reverse_lazy("tasks:list")
