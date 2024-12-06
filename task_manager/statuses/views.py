from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView
from .models import Status
from .forms import StatusForm
from task_manager.base_views import (BaseCreateView,
                                     BaseUpdateView,
                                     BaseDeleteView)
from django.utils.translation import gettext_lazy as _
from django.contrib import messages
from django.shortcuts import redirect


class StatusListView(LoginRequiredMixin, ListView):
    model = Status
    template_name = 'statuses/status_list.html'
    context_object_name = 'statuses'
    ordering = ['id']


class StatusCreateView(BaseCreateView):
    model = Status
    form_class = StatusForm
    template_name = 'statuses/status_form.html'
    success_url = reverse_lazy('statuses')
    success_message = _("Status successfully created")


class StatusUpdateView(BaseUpdateView):
    model = Status
    form_class = StatusForm
    template_name = 'statuses/status_form.html'
    success_url = reverse_lazy('statuses')
    success_message = _("Status successfully updated")


class StatusDeleteView(BaseDeleteView):
    model = Status
    template_name = 'statuses/status_confirm_delete.html'
    success_url = reverse_lazy('statuses')
    success_message = _("Status successfully deleted")

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        if self.object.task_set.exists():
            messages.error(
                request,
                _("Cannot delete status because it is in use"),
                extra_tags='danger'
            )
            return redirect('statuses')
        return super().post(request, *args, **kwargs)
