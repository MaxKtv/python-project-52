from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic import CreateView, UpdateView, DeleteView
from django.contrib import messages
from django.shortcuts import redirect
from django import forms
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _


class CustomFormWidgetMixin:
    """Миксин для добавления стилей к виджетам форм"""
    @staticmethod
    def get_form_widget(queryset):
        return forms.Select(attrs={'class': 'form-control'})


class CustomPermissionMixin(LoginRequiredMixin, UserPassesTestMixin):
    """Миксин для проверки прав доступа"""
    permission_message = None
    permission_url = None

    def handle_no_permission(self):
        if not self.request.user.is_authenticated:
            messages.error(
                self.request,
                _('You are not authorized! Please log in'),
                extra_tags='danger'
            )
            return redirect('login')
        messages.error(self.request, self.permission_message,
                       extra_tags='danger')
        return redirect(self.permission_url)


class CustomDeleteMixin(SuccessMessageMixin, DeleteView):
    """Базовый класс для представлений удаления"""
    template_name = None
    success_url = None
    success_message = None


class CustomCreateView(SuccessMessageMixin, CreateView):
    """Базовый класс для представлений создания"""
    template_name = None
    success_url = None
    success_message = None


class CustomUpdateView(CustomPermissionMixin, SuccessMessageMixin, UpdateView):
    """Базовый класс для представлений обновления"""
    template_name = None
    success_url = None
    success_message = None


class CustomLoginRequiredMixin(LoginRequiredMixin):
    """Базовый миксин для проверки аутентификации"""
    def handle_no_permission(self):
        messages.error(
            self.request,
            _('You are not authorized! Please log in'),
            extra_tags='danger'
        )
        return redirect('login')


class BaseCRUDTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser',
                                             password='password')
        self.client.login(username='testuser', password='password')

    def create_instance(self, model, url_name, data):
        self.client.post(reverse(url_name), data)
        self.assertEqual(model.objects.count(), 2)

    def update_instance(self, instance, url_name, data):
        self.client.post(reverse(url_name, args=[instance.pk]), data)
        instance.refresh_from_db()
        self.assertEqual(instance.name, data['name'])

    def delete_instance(self, model, instance, url_name):
        self.client.post(reverse(url_name, args=[instance.pk]))
        self.assertEqual(model.objects.count(), 0)


class BaseCUDView(LoginRequiredMixin, SuccessMessageMixin):
    model = None
    form_class = None
    template_name = None
    success_url = None
    success_message = None


class BaseCreateView(BaseCUDView, CreateView):
    pass


class BaseUpdateView(BaseCUDView, UpdateView):
    pass


class BaseDeleteView(BaseCUDView, DeleteView):
    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        if hasattr(self.object, 'task_set') and self.object.task_set.exists():
            messages.error(
                request,
                f"Невозможно удалить {self.model.__name__.lower()}, "
                f"потому что он используется",
                extra_tags='danger'
            )
            return redirect(self.success_url)
        return super().post(request, *args, **kwargs)
