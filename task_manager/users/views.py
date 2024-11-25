from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages
from django.shortcuts import redirect

class UserListView(ListView):
    model = User
    template_name = 'users/user_list.html'

class UserCreateView(SuccessMessageMixin, CreateView):
    model = User
    form_class = UserCreationForm
    template_name = 'users/register.html'
    success_url = reverse_lazy('login')
    success_message = "Пользователь успешно зарегистрирован"

class UserUpdateView(LoginRequiredMixin, UserPassesTestMixin, SuccessMessageMixin, UpdateView):
    model = User
    fields = ['username', 'first_name', 'last_name', 'email']
    template_name = 'users/user_form.html'
    success_url = reverse_lazy('user_list')
    success_message = "Пользователь успешно изменён"

    def test_func(self):
        return self.request.user.is_superuser

    def handle_no_permission(self):
        messages.add_message(
            self.request,
            messages.ERROR,
            "У вас нет прав для изменения пользователя",
            extra_tags='danger'
        )
        return redirect('user_list')

class UserDeleteView(LoginRequiredMixin, UserPassesTestMixin, SuccessMessageMixin, DeleteView):
    model = User
    template_name = 'users/user_confirm_delete.html'
    success_url = reverse_lazy('user_list')
    success_message = "Пользователь успешно удалён"

    def test_func(self):
        return self.request.user.is_superuser

    def handle_no_permission(self):
        messages.add_message(
            self.request,
            messages.ERROR,
            "У вас нет прав для удаления пользователя",
            extra_tags='danger'
        )
        return redirect('user_list')
