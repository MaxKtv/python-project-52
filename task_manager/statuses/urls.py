from task_manager.mixins.urls import get_crud_urlpatterns

from .views import (
    StatusCreateView,
    StatusDeleteView,
    StatusListView,
    StatusUpdateView,
)

app_name = 'statuses'

urlpatterns = get_crud_urlpatterns(
    StatusListView,
    StatusCreateView,
    StatusUpdateView,
    StatusDeleteView,
    ''
)
