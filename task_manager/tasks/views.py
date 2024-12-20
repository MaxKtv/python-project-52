from django.utils.translation import gettext_lazy as _
from django.views.generic import DetailView
from django_filters.views import FilterView

from task_manager.base import (
    AuthorPermissionMixin,
    AuthPermissionMixin,
    CreateView,
    DeleteView,
    UpdateView,
)

from .filter import TaskFilter
from .forms import TaskForm
from .models import Task


class TaskListView(AuthPermissionMixin, FilterView):
    """Представление для просмотра списка задач"""

    model = Task
    filterset_class = TaskFilter
    template_name = "tasks/task_list.html"
    context_object_name = "tasks"
    ordering = ["id"]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = _("Tasks")
        return context

    def get_filterset_kwargs(self, filterset_class):
        kwargs = super().get_filterset_kwargs(filterset_class)
        kwargs["request"] = self.request
        return kwargs


class TaskDetailView(AuthPermissionMixin, DetailView):
    """Представление для просмотра задачи"""

    model = Task
    template_name = "tasks/task_detail.html"
    context_object_name = "task"


class TaskCreateView(AuthPermissionMixin, CreateView):
    """Представление для создания задачи"""

    model = Task
    form_class = TaskForm
    template_name = "tasks/task_form.html"
    success_message = _("Task successfully created")

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class TaskUpdateView(AuthPermissionMixin, UpdateView):
    """Представление для обновления задачи"""

    model = Task
    form_class = TaskForm
    template_name = "tasks/task_form.html"
    success_message = _("Task successfully updated")


class TaskDeleteView(AuthorPermissionMixin, DeleteView):
    """Представление для удаления задачи"""

    model = Task
    template_name = "tasks/task_confirm_delete.html"
    success_message = _("Task successfully deleted")
