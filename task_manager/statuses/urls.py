from task_manager.base_urls import get_crud_urlpatterns
from .views import (StatusListView,
                    StatusCreateView,
                    StatusUpdateView,
                    StatusDeleteView)

urlpatterns = get_crud_urlpatterns(
    StatusListView,
    StatusCreateView,
    StatusUpdateView,
    StatusDeleteView,
    'statuses'
)
