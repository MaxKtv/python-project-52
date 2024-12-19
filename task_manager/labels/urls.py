from task_manager.tools import get_crud_urlpatterns

from .views import (
    LabelCreateView,
    LabelDeleteView,
    LabelListView,
    LabelUpdateView,
)

app_name = "labels"

urlpatterns = get_crud_urlpatterns(
    LabelListView, LabelCreateView, LabelUpdateView, LabelDeleteView, ""
)
