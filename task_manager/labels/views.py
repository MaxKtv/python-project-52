from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView
from .models import Label
from .forms import LabelForm
from task_manager.base_views import (BaseCreateView,
                                     BaseUpdateView,
                                     BaseDeleteView)
from django.utils.translation import gettext_lazy as _
from django.contrib import messages
from django.shortcuts import redirect


class LabelListView(LoginRequiredMixin, ListView):
    model = Label
    template_name = 'labels/label_list.html'
    context_object_name = 'labels'
    ordering = ['id']


class LabelCreateView(BaseCreateView):
    model = Label
    form_class = LabelForm
    template_name = 'labels/label_form.html'
    success_url = reverse_lazy('labels')
    success_message = _("Label successfully created")


class LabelUpdateView(BaseUpdateView):
    model = Label
    form_class = LabelForm
    template_name = 'labels/label_form.html'
    success_url = reverse_lazy('labels')
    success_message = _("Label successfully updated")


class LabelDeleteView(BaseDeleteView):
    model = Label
    template_name = 'labels/label_confirm_delete.html'
    success_url = reverse_lazy('labels')
    success_message = _("Label successfully deleted")

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        if self.object.task_set.exists():
            messages.error(
                request,
                _("Cannot delete label because it is in use"),
                extra_tags='danger'
            )
            return redirect('labels')
        return super().post(request, *args, **kwargs)
