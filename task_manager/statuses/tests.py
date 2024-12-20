from django.contrib.auth.models import User
from django.test import Client, TestCase
from django.urls import reverse

from task_manager.statuses.models import Status
from task_manager.tasks.models import Task


class StatusesTest(TestCase):
    fixtures = ['users.json', 'statuses.json']

    def setUp(self):
        self.client = Client()
        # Создаем тестового пользователя
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        # Создаем тестовый статус
        self.status = Status.objects.create(name='Test Status')
        # Создаем задачу, связанную со статусом
        self.task = Task.objects.create(
            name='Test Task',
            description='Test Description',
            status=self.status,
            author=self.user
        )

    def test_status_list_authenticated(self):
        """Тест просмотра списка статусов авторизованным пользователем."""
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('statuses:list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'statuses/status_list.html')

    def test_status_list_unauthenticated(self):
        """Тест просмотра списка статусов неавторизованным пользователем."""
        response = self.client.get(reverse('statuses:list'))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('login'))

    def test_status_create_authenticated(self):
        """Тест создания статуса авторизованным пользователем."""
        self.client.login(username='testuser', password='testpass123')
        response = self.client.post(reverse('statuses:create'), {
            'name': 'New Status'
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Status.objects.filter(name='New Status').exists())

    def test_status_create_unauthenticated(self):
        """Тест создания статуса неавторизованным пользователем."""
        response = self.client.post(reverse('statuses:create'), {
            'name': 'New Status'
        })
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Status.objects.filter(name='New Status').exists())

    def test_status_update_authenticated(self):
        """Тест обновления статуса авторизованным пользователем."""
        self.client.login(username='testuser', password='testpass123')
        response = self.client.post(
            reverse('statuses:update', kwargs={'pk': self.status.pk}),
            {'name': 'Updated Status'}
        )
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Status.objects.filter(name='Updated Status').exists())

    def test_status_update_unauthenticated(self):
        """Тест обновления статуса неавторизованным пользователем."""
        response = self.client.post(
            reverse('statuses:update', kwargs={'pk': self.status.pk}),
            {'name': 'Updated Status'}
        )
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Status.objects.filter(name='Updated Status').exists())

    def test_status_delete_with_task(self):
        """Тест удаления статуса, связанного с задачей."""
        self.client.login(username='testuser', password='testpass123')
        response = self.client.post(
            reverse('statuses:delete', kwargs={'pk': self.status.pk})
        )
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Status.objects.filter(pk=self.status.pk).exists())

    def test_status_delete_without_task(self):
        """Тест удаления статуса без связанных задач."""
        self.client.login(username='testuser', password='testpass123')
        new_status = Status.objects.create(name='Status to Delete')
        response = self.client.post(
            reverse('statuses:delete', kwargs={'pk': new_status.pk})
        )
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Status.objects.filter(pk=new_status.pk).exists())
