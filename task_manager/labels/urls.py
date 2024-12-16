from task_manager.mixins.urls import get_crud_urlpatterns
from .views import (LabelListView,
                    LabelCreateView,
                    LabelUpdateView,
                    LabelDeleteView)

app_name = 'labels'

urlpatterns = get_crud_urlpatterns(
    LabelListView,
    LabelCreateView,
    LabelUpdateView,
    LabelDeleteView,
    ''
)
