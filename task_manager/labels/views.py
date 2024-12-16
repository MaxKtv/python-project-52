from django.utils.translation import gettext_lazy as _

from task_manager.mixins import ListView, CreateView, UpdateView, DeleteView
from .models import Label
from .forms import LabelForm


class LabelListView(ListView):
    """Представление для просмотра списка меток"""
    model = Label
    title = _('Labels')
    template_name = 'labels/label_list.html'
    context_object_name = 'labels'


class LabelCreateView(CreateView):
    """Представление для создания метки"""
    model = Label
    form_class = LabelForm
    success_message = _("Label successfully created")


class LabelUpdateView(UpdateView):
    """Представление для обновления метки"""
    model = Label
    form_class = LabelForm
    success_message = _("Label successfully updated")


class LabelDeleteView(DeleteView):
    """Представление для удаления метки"""
    model = Label
    template_name = 'labels/label_confirm_delete.html'
    protected_message = _("Cannot delete label because it's in use")
    success_message = _("Label successfully deleted")
