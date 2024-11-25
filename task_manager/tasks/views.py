from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib import messages
from django_filters.views import FilterView
from django.shortcuts import redirect
from .models import Task
from .forms import TaskForm
from .filter import TaskFilter


class TaskListView(LoginRequiredMixin, FilterView):
    model = Task
    filterset_class = TaskFilter
    template_name = 'tasks/task_list.html'
    context_object_name = 'tasks'


class TaskDetailView(LoginRequiredMixin, DetailView):
    model = Task
    template_name = 'tasks/task_detail.html'
    context_object_name = 'task'


class TaskCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Task
    form_class = TaskForm
    template_name = 'tasks/task_form.html'
    success_url = reverse_lazy('tasks')
    success_message = "Задача успешно создана"

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class TaskUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Task
    form_class = TaskForm
    template_name = 'tasks/task_form.html'
    success_url = reverse_lazy('tasks')
    success_message = "Задача успешно обновлена"


class TaskDeleteView(LoginRequiredMixin, UserPassesTestMixin, SuccessMessageMixin, DeleteView):
    model = Task
    template_name = 'tasks/task_confirm_delete.html'
    success_url = reverse_lazy('tasks')
    success_message = "Задача успешно удалена"

    def test_func(self):
        return self.get_object().author == self.request.user

    def handle_no_permission(self):
        messages.add_message(
            self.request,
            messages.ERROR,
            "Задачу может удалить только её автор",
            extra_tags='danger'
        )
        return redirect('tasks')
