from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path
from . import views

urlpatterns = [
    path('create/', views.UserCreateView.as_view(), name='user_create'),
    path('<int:pk>/update/', views.UserUpdateView.as_view(), name='user_update'),
    path('<int:pk>/delete/', views.UserDeleteView.as_view(), name='user_delete'),
    path('', views.UserListView.as_view(), name='user_list'),
]
