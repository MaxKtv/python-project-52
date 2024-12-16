from django.urls import path


def get_crud_urlpatterns(list_view,
                         create_view,
                         update_view,
                         delete_view,
                         base_name):

    return [
        path('', list_view.as_view(), name='list'),
        path('create/', create_view.as_view(), name='create'),
        path('<int:pk>/update/', update_view.as_view(), name='update'),
        path('<int:pk>/delete/', delete_view.as_view(), name='delete'),
    ]
