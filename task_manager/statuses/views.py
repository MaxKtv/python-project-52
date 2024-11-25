from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404
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


class StatusDeleteView(LoginRequiredMixin, DeleteView):
    model = Status
    template_name = 'statuses/status_confirm_delete.html'
    success_url = reverse_lazy('statuses')

    def form_valid(self, form):
        try:
            return super().form_valid(form)
        except models.ProtectedError:
            messages.error(self.request, "Нельзя удалить статус, связанный с задачами.")
            return self.render_to_response(self.get_context_data(form=form))

