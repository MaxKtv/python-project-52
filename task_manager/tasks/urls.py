from django.urls import path
from task_manager.mixins.urls import get_crud_urlpatterns

from .views import (
    TaskCreateView,
    TaskDeleteView,
    TaskDetailView,
    TaskListView,
    TaskUpdateView,
)

app_name = 'tasks'

# Основные CRUD URL'ы
crud_patterns = get_crud_urlpatterns(
    TaskListView,
    TaskCreateView,
    TaskUpdateView,
    TaskDeleteView,
    ''
)

# Добавляем URL для детального просмотра
urlpatterns = crud_patterns + [
    path('<int:pk>/', TaskDetailView.as_view(), name='detail'),
]
