from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import DetailView
from django.contrib import messages
from django_filters.views import FilterView
from .models import Task
from .forms import TaskForm
from .filter import TaskFilter
from task_manager.base_views import (BaseCreateView,
                                     BaseUpdateView,
                                     BaseDeleteView)
from django.shortcuts import redirect
from django.utils.translation import gettext_lazy as _


class TaskListView(LoginRequiredMixin, FilterView):
    model = Task
    filterset_class = TaskFilter
    template_name = 'tasks/task_list.html'
    context_object_name = 'tasks'
    ordering = ['id']


class TaskDetailView(LoginRequiredMixin, DetailView):
    model = Task
    template_name = 'tasks/task_detail.html'
    context_object_name = 'task'


class TaskCreateView(BaseCreateView):
    model = Task
    form_class = TaskForm
    template_name = 'tasks/task_form.html'
    success_url = reverse_lazy('tasks')
    success_message = _("Task successfully created")

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class TaskUpdateView(BaseUpdateView):
    model = Task
    form_class = TaskForm
    template_name = 'tasks/task_form.html'
    success_url = reverse_lazy('tasks')
    success_message = _("Task successfully updated")


class TaskDeleteView(BaseDeleteView):
    model = Task
    success_url = reverse_lazy('tasks')
    template_name = 'tasks/task_confirm_delete.html'
    success_message = _('Task successfully deleted')

    def dispatch(self, request, *args, **kwargs):
        task = self.get_object()
        if task.author != request.user:
            messages.error(
                request,
                _("Task can only be deleted by its author"),
                extra_tags='danger'
            )
            return redirect(self.success_url)
        return super().dispatch(request, *args, **kwargs)
