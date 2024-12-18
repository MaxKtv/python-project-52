from task_manager.mixins.urls import get_crud_urlpatterns

from . import views

app_name = 'users'

urlpatterns = get_crud_urlpatterns(
    list_view=views.UserListView,
    create_view=views.UserCreateView,
    update_view=views.UserUpdateView,
    delete_view=views.UserDeleteView,
    base_name=''
)
