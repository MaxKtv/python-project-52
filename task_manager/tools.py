from django.forms import Select
from django.urls import path


FORM_CONTROL_ATTRS = {"class": "form-control"}


def get_form_widget(queryset=None):
    """Возвращает виджет формы"""
    widget = Select(attrs=FORM_CONTROL_ATTRS)
    if queryset:
        widget.choices = [(obj.pk, str(obj)) for obj in queryset]
    return widget


def get_crud_urlpatterns(
    list_view, create_view, update_view, delete_view, base_name
):
    return [
        path("", list_view.as_view(), name="list"),
        path("create/", create_view.as_view(), name="create"),
        path("<int:pk>/update/", update_view.as_view(), name="update"),
        path("<int:pk>/delete/", delete_view.as_view(), name="delete"),
    ]


def get_user_full_name(obj):
    """Возвращает полное имя пользователя"""
    full_name = f"{obj.first_name} {obj.last_name}".strip()
    return full_name if full_name else obj.username


def is_in_tasks(obj, named_model):
    """Проверка на наличие объекта в задачах"""
    if isinstance(obj, named_model):
        if hasattr(obj, "task_set") and obj.task_set.exists():
            return True
    return False
