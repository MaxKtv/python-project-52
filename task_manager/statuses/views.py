from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.views.generic.list import ListView

from task_manager.mixins import AuthPermissionMixin, ProtectedMessageMixin

from .forms import StatusForm
from .models import Status


class StatusListView(AuthPermissionMixin, ListView):
    """Представление для просмотра списка статусов"""

    model = Status
    title = _("Statuses")
    context_object_name = "statuses"
    success_url = reverse_lazy("statuses:list")
    ordering = ["id"]


class StatusCreateView(AuthPermissionMixin, SuccessMessageMixin, CreateView):
    """Представление для создания статуса"""

    model = Status
    form_class = StatusForm
    success_url = reverse_lazy("statuses:list")
    success_message = _("Status successfully created")


class StatusUpdateView(AuthPermissionMixin, SuccessMessageMixin, UpdateView):
    """Представление для обновления статуса"""

    model = Status
    form_class = StatusForm
    success_url = reverse_lazy("statuses:list")
    success_message = _("Status successfully updated")


class StatusDeleteView(AuthPermissionMixin, ProtectedMessageMixin, DeleteView):
    """Представление для удаления статуса"""

    model = Status
    success_url = reverse_lazy("statuses:list")
    success_message = _("Status successfully deleted")
    protected_message = _("Cannot delete status because it's in use")
