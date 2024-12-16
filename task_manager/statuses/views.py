from django.utils.translation import gettext_lazy as _
from django.urls import reverse_lazy

from task_manager.mixins import (
    ListView, CreateView, UpdateView, DeleteView,
)
from .models import Status
from .forms import StatusForm


class StatusListView(ListView):
    """Представление для просмотра списка статусов"""
    model = Status
    title = _('Statuses')
    context_object_name = 'statuses'


class StatusCreateView(CreateView):
    """Представление для создания статуса"""
    model = Status
    form_class = StatusForm
    success_message = _("Status successfully created")


class StatusUpdateView(UpdateView):
    """Представление для обновления статуса"""
    model = Status
    form_class = StatusForm
    success_message = _("Status successfully updated")


class StatusDeleteView(DeleteView):
    """Представление для удаления статуса"""
    model = Status
    template_name = 'statuses/status_confirm_delete.html'
    protected_message = _("Cannot delete status because it's in use")
    protected_url = reverse_lazy('statuses:list')
    success_message = _("Status successfully deleted")
