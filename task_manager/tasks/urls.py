from django.urls import path

from task_manager.tools import get_crud_urlpatterns

from .views import (
    TaskCreateView,
    TaskDeleteView,
    TaskDetailView,
    TaskListView,
    TaskUpdateView,
)

app_name = "tasks"


crud_patterns = get_crud_urlpatterns(
    TaskListView, TaskCreateView, TaskUpdateView, TaskDeleteView, ""
)

urlpatterns = crud_patterns + [
    path("<int:pk>/", TaskDetailView.as_view(), name="detail"),
]
