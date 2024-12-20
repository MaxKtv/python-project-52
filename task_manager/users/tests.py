from django.contrib.auth.models import User
from django.test import Client, TestCase
from django.urls import reverse

from task_manager.statuses.models import Status
from task_manager.tasks.models import Task


class UsersTest(TestCase):
    fixtures = ['users.json']

    def setUp(self):
        self.client = Client()
        # Создаем тестовых пользователей
        self.test_user = User.objects.create_user(
            username='newuser',
            password='testpass123',
            first_name='Test',
            last_name='User'
        )

        self.test_user2 = User.objects.create_user(
            username='newuser2',
            password='testpass123',
            first_name='Test2',
            last_name='User2'
        )

        # Создаем статус и задачу для тестирования защиты от удаления
        self.status = Status.objects.create(name='Test Status')
        self.task = Task.objects.create(
            name='Test Task',
            description='Test Description',
            status=self.status,
            author=self.test_user,
            executor=self.test_user
        )

    def test_users_list(self):
        """Тест просмотра списка пользователей."""
        response = self.client.get(reverse('users:list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/user_list.html')

    def test_user_create(self):
        """Тест создания пользователя."""
        response = self.client.post(reverse('users:create'), {
            'username': 'testuser3',
            'password1': 'testpass123',
            'password2': 'testpass123',
            'first_name': 'Test',
            'last_name': 'User'
        })
        self.assertRedirects(response, reverse('login'))
        self.assertTrue(User.objects.filter(username='testuser3').exists())

    def test_user_update(self):
        """Тест обновления пользователя."""
        self.client.login(username='newuser', password='testpass123')
        response = self.client.post(
            reverse('users:update', kwargs={'pk': self.test_user.pk}),
            {
                'username': 'updated_user',
                'first_name': 'Updated',
                'last_name': 'User',
                'password1': 'newpass123',
                'password2': 'newpass123'
            }
        )
        self.assertRedirects(response, reverse('users:list'))
        updated_user = User.objects.get(pk=self.test_user.pk)
        self.assertEqual(updated_user.username, 'updated_user')
        self.assertEqual(updated_user.first_name, 'Updated')

    def test_user_delete(self):
        """Тест удаления пользователя."""
        # Тест 1: Пользователь с задачами не может быть удален
        self.client.login(username='newuser', password='testpass123')
        response = self.client.post(
            reverse('users:delete', kwargs={'pk': self.test_user.pk})
        )
        self.assertRedirects(response, reverse('users:list'))
        self.assertTrue(User.objects.filter(pk=self.test_user.pk).exists())

        # Тест 2: Пользователь без задач может быть удален
        self.client.login(username='newuser2', password='testpass123')
        response = self.client.post(
            reverse('users:delete', kwargs={'pk': self.test_user2.pk})
        )
        self.assertRedirects(response, reverse('users:list'))
        self.assertFalse(User.objects.filter(pk=self.test_user2.pk).exists())
