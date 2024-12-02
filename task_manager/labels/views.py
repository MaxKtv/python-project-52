from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib import messages
from django.shortcuts import redirect
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


class LabelDeleteView(LoginRequiredMixin, SuccessMessageMixin, DeleteView):
    model = Label
    template_name = 'labels/label_confirm_delete.html'
    success_url = reverse_lazy('labels')
    success_message = "Метка успешно удалена"

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        if self.object.task_set.exists():
            messages.error(
                request,
                "Невозможно удалить метку, потому что она используется",
                extra_tags='danger'
            )
            return redirect('labels')
        return super().post(request, *args, **kwargs)
