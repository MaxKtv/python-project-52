from django.urls import path


def get_crud_urlpatterns(list_view,
                         create_view,
                         update_view,
                         delete_view,
                         base_name):
    return [
        path('', list_view.as_view(), name=base_name),
        path('create/', create_view.as_view(), name=f'{base_name}_create'),
        path('<int:pk>/update/', update_view.as_view(),
             name=f'{base_name}_update'),
        path('<int:pk>/delete/', delete_view.as_view(),
             name=f'{base_name}_delete'),
    ]
