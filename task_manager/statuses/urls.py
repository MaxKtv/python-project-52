from task_manager.mixins.urls import get_crud_urlpatterns
from .views import (StatusListView,
                    StatusCreateView,
                    StatusUpdateView,
                    StatusDeleteView)

app_name = 'statuses'

urlpatterns = get_crud_urlpatterns(
    StatusListView,
    StatusCreateView,
    StatusUpdateView,
    StatusDeleteView,
    ''
)
