from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.db.models.deletion import ProtectedError
from django.shortcuts import redirect
from django.utils.translation import gettext_lazy as _
from django.views.generic import ListView as DjangoListView
from django.views.generic import CreateView as DjangoCreateView
from django.views.generic import UpdateView as DjangoUpdateView
from django.views.generic import DeleteView as DjangoDeleteView

from .base import BaseViewMixin
from .forms import FormWidgetMixin


class ListView(BaseViewMixin, DjangoListView):
    """Базовый класс для отображения списков"""
    template_name_suffix = '_list'
    _context_object_name = None
    ordering = ['id']

    @property
    def context_object_name(self):
        """Возвращает имя переменной контекста для списка объектов"""
        if self._context_object_name is None:
            self._context_object_name = self.model._meta.model_name + 's'
        return self._context_object_name


class CreateView(BaseViewMixin,
                 FormWidgetMixin,
                 SuccessMessageMixin,
                 DjangoCreateView):
    """Базовый класс для создания объектов"""
    template_name_suffix = '_form'


class UpdateView(BaseViewMixin,
                 FormWidgetMixin,
                 SuccessMessageMixin,
                 DjangoUpdateView):
    """Базовый класс для обновления объектов"""
    template_name_suffix = '_form'


class DeleteView(BaseViewMixin, DjangoDeleteView):
    """Базовый класс для удаления объектов"""
    template_name_suffix = '_confirm_delete'
    protected_message = _("Cannot delete this object because "
                          "it's referenced by other objects.")
    protected_url = None

    def post(self, request, *args, **kwargs):
        """Обработка POST-запроса"""
        try:
            response = super().post(request, *args, **kwargs)
            messages.success(request, self.success_message)
            return response
        except ProtectedError:
            messages.error(request, self.protected_message)
            return redirect(self.protected_url or self.get_success_url())
