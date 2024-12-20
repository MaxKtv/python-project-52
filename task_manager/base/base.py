from django import forms
from django.contrib import messages
from django.core.exceptions import PermissionDenied
from django.db import DatabaseError, models
from django.http import Http404
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

# Константы для сообщений
SUCCESS_MESSAGES = {
    "create": _("created"),
    "update": _("updated"),
    "delete": _("deleted"),
}


class NamedModelMeta(models.base.ModelBase):
    """Метакласс устанавливает verbose_name и verbose_name_plural"""

    def __new__(cls, name, bases, attrs):
        # Создаем класс модели
        new_class = super().__new__(cls, name, bases, attrs)
        if not new_class._meta.abstract:
            new_class._meta.unique_together = [["name"]]
        return new_class

        # Получаем или создаем Meta
        meta = attrs.get("Meta", type("Meta", (), {}))

        # Устанавливаем значения только если они не определены
        if not hasattr(meta, "verbose_name"):
            meta.verbose_name = _(name)
        if not hasattr(meta, "verbose_name_plural"):
            meta.verbose_name_plural = _(f"{name}s")

        # Обновляем Meta в новом классе
        new_class._meta.verbose_name = meta.verbose_name
        new_class._meta.verbose_name_plural = meta.verbose_name_plural

        return new_class


class NamedModel(models.Model, metaclass=NamedModelMeta):
    """Базовый класс для моделей с полями name и created_at"""

    name = models.CharField(max_length=100, verbose_name=_("Name"))
    created_at = models.DateTimeField(
        default=timezone.now, editable=False, verbose_name=_("Created at")
    )

    def __str__(self):
        return self.name

    def delete(self, *args, **kwargs):
        """Проверяет, можно ли удалить объект"""
        if hasattr(self, "task_set") and self.task_set.exists():
            raise models.ProtectedError(
                _("Cannot delete %(model)s because it's in use")
                % {"model": self._meta.verbose_name.lower()},
                self,
            )
        return super().delete(*args, **kwargs)

    class Meta:
        abstract = True


class BaseView:
    """Базовый класс для всех представлений"""

    title = None
    success_message = None
    action_type = "create"  # По умолчанию создание

    def get_context_data(self, **kwargs):
        """Добавляет заголовок в контекст"""
        context = super().get_context_data(**kwargs)
        if self.title is None:
            model_name = self.model._meta.verbose_name
            if hasattr(self, "object") and self.object:
                self.title = _("Edit {model_name}").format(
                    model_name=model_name
                )
            else:
                self.title = _("Create {model_name}").format(
                    model_name=model_name
                )
        context["title"] = self.title
        return context

    @property
    def template_name(self):
        """Автоматически генерирует имя шаблона"""
        if not hasattr(self, "_template_name"):
            app_label = self.model._meta.app_label
            model_name = self.model._meta.model_name
            self._template_name = (
                f"{app_label}/{model_name}{self.template_name_suffix}.html"
            )
        return self._template_name

    def get_success_url(self):
        """URL для перенаправления после успешной операции"""
        if not hasattr(self, "_success_url"):
            app_label = self.model._meta.app_label
            model_name = self.model._meta.model_name
            if app_label == "auth" and model_name == "user":
                self._success_url = reverse_lazy("users:list")
            else:
                self._success_url = reverse_lazy(f"{app_label}:list")
        return self._success_url

    def get_success_message(self, cleaned_data=None):
        """Get success message for the view."""
        if self.success_message is None:
            model_name = self.model._meta.verbose_name
            action = SUCCESS_MESSAGES.get(
                self.action_type, SUCCESS_MESSAGES["create"]
            )
            self.success_message = _(
                "{model_name} successfully " "{action}"
            ).format(model_name=model_name, action=action)
        return self.success_message

    def handle_not_found(self):
        """Обработка ошибки 404 (объект не найден)"""
        raise Http404(_("The requested resource was not found."))

    def handle_permission_denied(self):
        """Обработка ошибки прав доступа (403)"""
        messages.error(
            self.request,
            _("You don't have permission to access this resource.")
        )
        return self.redirect("home")

    def handle_server_error(self):
        """Обработка ошибки 500 (внутренняя ошибка сервера)"""
        messages.error(
            self.request,
            _("An internal server error occurred. Please try again later.")
        )
        return self.redirect("home")

    def dispatch(self, request, *args, **kwargs):
        try:
            # Здесь вызов метода, который фактически выполняет представление
            return super().dispatch(request, *args, **kwargs)
        except Http404:
            return self.handle_not_found()
        except PermissionDenied:
            return self.handle_permission_denied()
        except DatabaseError:
            return self.handle_server_error()
        except Exception as e:
            print(f"Unexpected error: {e}")
            return self.handle_server_error()

    @staticmethod
    def redirect(self, url_name):
        """Переход на URL с именем"""
        return redirect(reverse_lazy(url_name))


class BaseNameModelForm(forms.ModelForm):
    """Базовый класс формы для моделей с полем name"""

    name = forms.CharField(
        label=_("Name"), widget=forms.TextInput(attrs={"class": "form-control"})
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if isinstance(field, forms.ModelChoiceField):
                field.label_from_instance = self.get_label_from_instance

    def get_label_from_instance(self, obj):
        """Настраиваем отображение вариантов для ModelChoiceField"""
        if hasattr(obj, "first_name") and hasattr(obj, "last_name"):
            full_name = f"{obj.first_name} {obj.last_name}".strip()
            return full_name if full_name else obj.username
        return str(obj)
