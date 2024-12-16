from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic import CreateView, UpdateView, DeleteView
from django.contrib import messages
from django.shortcuts import redirect
from django.utils.translation import gettext_lazy as _


class BaseCUDView(LoginRequiredMixin, SuccessMessageMixin):
    model = None
    form_class = None
    template_name = None
    success_url = None
    success_message = None

    def handle_no_permission(self):
        messages.error(
            self.request,
            _("You are not authorized! Please log in."),
            extra_tags='danger'
        )
        return super().handle_no_permission()


class BaseCreateView(BaseCUDView, CreateView):
    pass


class BaseUpdateView(BaseCUDView, UpdateView):
    pass


class BaseDeleteView(BaseCUDView, DeleteView):
    def get_form(self, form_class=None):
        return None

    def get_form_class(self):
        return None

    def get_form_kwargs(self):
        return {}

    def get_context_data(self, **kwargs):
        return {
            'view': self,
            'object': self.object,
        }

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        if hasattr(self.object, 'task_set') and self.object.task_set.exists():
            messages.error(
                request,
                _("Cannot delete %(name)s because it is in use") % {
                    'name': self.model.__name__.lower()
                },
                extra_tags='danger'
            )
            return redirect(self.success_url)

        success_url = self.get_success_url()
        self.object.delete()
        if self.success_message:
            messages.success(request, self.success_message)
        return redirect(success_url)
