from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.contrib import messages
from .models import Status
from .forms import StatusForm


class StatusListView(LoginRequiredMixin, ListView):
    model = Status
    template_name = 'statuses/status_list.html'
    context_object_name = 'statuses'


class StatusCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Status
    form_class = StatusForm
    template_name = 'statuses/status_form.html'
    success_url = reverse_lazy('statuses')
    success_message = "Статус успешно создан."


class StatusUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Status
    form_class = StatusForm
    template_name = 'statuses/status_form.html'
    success_url = reverse_lazy('statuses')
    success_message = "Статус успешно обновлен."


class StatusDeleteView(LoginRequiredMixin, SuccessMessageMixin, DeleteView):
    model = Status
    template_name = 'statuses/status_confirm_delete.html'
    success_url = reverse_lazy('statuses')
    success_message = "Статус успешно удалён"

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        if self.object.task_set.exists():
            messages.error(
                request,
                "Невозможно удалить статус, потому что он используется",
                extra_tags='danger'
            )
            return redirect('statuses')
        return super().post(request, *args, **kwargs)
