from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy

class UserListView(ListView):
    model = User
    template_name = 'users/user_list.html'

class UserCreateView(CreateView):
    model = User
    form_class = UserCreationForm
    template_name = 'users/register.html'
    success_url = reverse_lazy('login')

class UserUpdateView(UpdateView):
    model = User
    fields = ['username', 'first_name', 'last_name', 'email']
    template_name = 'users/user_form.html'
    success_url = reverse_lazy('user_list')

class UserDeleteView(DeleteView):
    model = User
    template_name = 'users/user_confirm_delete.html'
    success_url = reverse_lazy('user_list')

