from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.db import models
from django.utils import timezone


# Константы для сообщений
SUCCESS_MESSAGES = {
    'create': _('created'),
    'update': _('updated'),
    'delete': _('deleted')
}


class NamedModelMeta(models.base.ModelBase):
    """Метакласс устанавливает verbose_name и verbose_name_plural"""

    def __new__(cls, name, bases, attrs):
        # Создаем класс модели
        new_class = super().__new__(cls, name, bases, attrs)

        # Получаем или создаем Meta
        meta = attrs.get('Meta', type('Meta', (), {}))

        # Устанавливаем значения только если они не определены
        if not hasattr(meta, 'verbose_name'):
            meta.verbose_name = _(name)
        if not hasattr(meta, 'verbose_name_plural'):
            meta.verbose_name_plural = _(f'{name}s')

        # Обновляем Meta в новом классе
        new_class._meta.verbose_name = meta.verbose_name
        new_class._meta.verbose_name_plural = meta.verbose_name_plural

        return new_class


class NamedModel(models.Model, metaclass=NamedModelMeta):
    """Базовый класс для моделей с полями name и created_at"""
    name = models.CharField(max_length=100, verbose_name=_('Name'))
    created_at = models.DateTimeField(default=timezone.now,
                                      editable=False,
                                      verbose_name=_('Created at'))

    def __str__(self):
        return self.name

    def delete(self, *args, **kwargs):
        """Проверяет, можно ли удалить объект"""
        if hasattr(self, 'task_set') and self.task_set.exists():
            raise models.ProtectedError(
                _("Cannot delete %(model)s because it's in use")
                % {'model': self._meta.verbose_name.lower()}, self
            )
        return super().delete(*args, **kwargs)

    class Meta:
        abstract = True
        unique_together = [['name']]  # Общее требование уникальности имени


class BaseViewMixin:
    """Базовый миксин для всех представлений"""
    title = None
    success_message = None
    action_type = 'create'  # По умолчанию создание

    def get_context_data(self, **kwargs):
        """Добавляет заголовок в контекст"""
        context = super().get_context_data(**kwargs)
        if self.title is None:
            model_name = self.model._meta.verbose_name
            if hasattr(self, 'object') and self.object:
                self.title = _('Edit {model_name}').format(
                    model_name=model_name
                )
            else:
                self.title = _('Create {model_name}').format(
                    model_name=model_name
                )
        context['title'] = self.title
        return context

    @property
    def template_name(self):
        """Автоматически генерирует имя шаблона"""
        if not hasattr(self, '_template_name'):
            app_label = self.model._meta.app_label
            model_name = self.model._meta.model_name
            self._template_name = (
                f'{app_label}/{model_name}{self.template_name_suffix}.html'
            )
        return self._template_name

    def get_success_url(self):
        """URL для перенаправления после успешной операции"""
        if not hasattr(self, '_success_url'):
            app_label = self.model._meta.app_label
            if app_label == 'users':
                self._success_url = reverse_lazy('users')
            else:
                self._success_url = reverse_lazy(f'{app_label}:list')
        return self._success_url

    def get_success_message(self, cleaned_data=None):
        """Get success message for the view."""
        if self.success_message is None:
            model_name = self.model._meta.verbose_name
            action = SUCCESS_MESSAGES.get(
                self.action_type,
                SUCCESS_MESSAGES['create']
            )
            self.success_message = _('{model_name} successfully '
                                     '{action}').format(
                model_name=model_name,
                action=action
            )
        return self.success_message
