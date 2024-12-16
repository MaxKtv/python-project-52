from .auth import (
    AuthMixin,
    UserPermissionMixin,
    SuperuserRequiredMixin,
    TaskAuthorRequiredMixin
)
from .forms import FormWidgetMixin, BaseNameModelForm
from .base import BaseViewMixin, NamedModel
from .testing import BaseCRUDTest
from .urls import get_crud_urlpatterns
from .views import (
    ListView,
    CreateView,
    UpdateView,
    DeleteView
)


__all__ = [
    'AuthMixin',
    'UserPermissionMixin',
    'SuperuserRequiredMixin',
    'TaskAuthorRequiredMixin',
    'FormWidgetMixin',
    'BaseNameModelForm',
    'BaseViewMixin',
    'NamedModel',
    'BaseCRUDTest',
    'get_crud_urlpatterns',
    'ListView',
    'CreateView',
    'UpdateView',
    'DeleteView'
]
