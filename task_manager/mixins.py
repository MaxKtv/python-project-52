from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic import CreateView, UpdateView, DeleteView
from django.contrib import messages
from django.shortcuts import redirect
from django import forms


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
                'Вы не авторизованы! Пожалуйста, выполните вход',
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
            'Вы не авторизованы! Пожалуйста, выполните вход',
            extra_tags='danger'
        )
        return redirect('login')
