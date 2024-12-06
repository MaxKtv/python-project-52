from task_manager.base_urls import get_crud_urlpatterns
from .views import (LabelListView,
                    LabelCreateView,
                    LabelUpdateView,
                    LabelDeleteView)

urlpatterns = get_crud_urlpatterns(
    LabelListView,
    LabelCreateView,
    LabelUpdateView,
    LabelDeleteView,
    'labels'
)
