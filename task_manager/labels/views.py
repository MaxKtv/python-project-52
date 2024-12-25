from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.views.generic.list import ListView

from task_manager.mixins import AuthPermissionMixin, ProtectedMessageMixin

from .forms import LabelForm
from .models import Label


class LabelListView(AuthPermissionMixin, ListView):
    """Представление для просмотра списка меток"""

    model = Label
    template_name = "labels/label_list.html"
    context_object_name = "labels"
    ordering = ["id"]


class LabelCreateView(AuthPermissionMixin, SuccessMessageMixin, CreateView):
    """Представление для создания метки"""

    model = Label
    form_class = LabelForm
    success_message = _("Label successfully created")
    success_url = reverse_lazy("labels:list")


class LabelUpdateView(AuthPermissionMixin, SuccessMessageMixin, UpdateView):
    """Представление для обновления метки"""

    model = Label
    form_class = LabelForm
    success_message = _("Label successfully updated")
    success_url = reverse_lazy("labels:list")


class LabelDeleteView(AuthPermissionMixin, ProtectedMessageMixin, DeleteView):
    """Представление для удаления метки"""

    model = Label
    template_name = "labels/label_confirm_delete.html"
    protected_message = _("Cannot delete label because it's in use")
    success_message = _("Label successfully deleted")
    success_url = reverse_lazy("labels:list")
