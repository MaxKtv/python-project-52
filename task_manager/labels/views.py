from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib import messages
from django.db import models
from .models import Label
from .forms import LabelForm


class LabelListView(LoginRequiredMixin, ListView):
    model = Label
    template_name = 'labels/label_list.html'
    context_object_name = 'labels'


class LabelCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Label
    form_class = LabelForm
    template_name = 'labels/label_form.html'
    success_url = reverse_lazy('labels')
    success_message = "Метка успешно создана."


class LabelUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Label
    form_class = LabelForm
    template_name = 'labels/label_form.html'
    success_url = reverse_lazy('labels')
    success_message = "Метка успешно обновлена."


class LabelDeleteView(LoginRequiredMixin, DeleteView):
    model = Label
    template_name = 'labels/label_confirm_delete.html'
    success_url = reverse_lazy('labels')

    def form_valid(self, form):
        try:
            return super().form_valid(form)
        except models.ProtectedError:
            messages.error(self.request, "Нельзя удалить метку, связанную с задачами.")
            return self.render_to_response(self.get_context_data(form=form))
