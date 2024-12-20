from django.contrib.auth.models import User
from django.test import Client, TestCase
from django.urls import reverse

from task_manager.labels.models import Label
from task_manager.statuses.models import Status
from task_manager.tasks.models import Task


class LabelsTest(TestCase):
    fixtures = ['users.json', 'labels.json']

    def setUp(self):
        self.client = Client()
        # Создаем тестового пользователя
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        # Создаем тестовый статус
        self.status = Status.objects.create(name='Test Status')
        # Создаем тестовую метку
        self.label = Label.objects.create(name='Test Label')
        # Создаем задачу с меткой
        self.task = Task.objects.create(
            name='Test Task',
            description='Test Description',
            status=self.status,
            author=self.user
        )
        self.task.labels.add(self.label)

    def test_label_list_authenticated(self):
        """Тест просмотра списка меток авторизованным пользователем."""
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('labels:list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'labels/label_list.html')

    def test_label_list_unauthenticated(self):
        """Тест просмотра списка меток неавторизованным пользователем."""
        response = self.client.get(reverse('labels:list'))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('login'))

    def test_label_create_authenticated(self):
        """Тест создания метки авторизованным пользователем."""
        self.client.login(username='testuser', password='testpass123')
        response = self.client.post(reverse('labels:create'), {
            'name': 'New Label'
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Label.objects.filter(name='New Label').exists())

    def test_label_create_unauthenticated(self):
        """Тест создания метки неавторизованным пользователем."""
        response = self.client.post(reverse('labels:create'), {
            'name': 'New Label'
        })
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Label.objects.filter(name='New Label').exists())

    def test_label_update_authenticated(self):
        """Тест обновления метки авторизованным пользователем."""
        self.client.login(username='testuser', password='testpass123')
        response = self.client.post(
            reverse('labels:update', kwargs={'pk': self.label.pk}),
            {'name': 'Updated Label'}
        )
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Label.objects.filter(name='Updated Label').exists())

    def test_label_update_unauthenticated(self):
        """Тест обновления метки неавторизованным пользователем."""
        response = self.client.post(
            reverse('labels:update', kwargs={'pk': self.label.pk}),
            {'name': 'Updated Label'}
        )
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Label.objects.filter(name='Updated Label').exists())

    def test_label_delete_with_task(self):
        """Тест удаления метки, связанной с задачей."""
        self.client.login(username='testuser', password='testpass123')
        response = self.client.post(
            reverse('labels:delete', kwargs={'pk': self.label.pk})
        )
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Label.objects.filter(pk=self.label.pk).exists())

    def test_label_delete_without_task(self):
        """Тест удаления метки без связанных задач."""
        self.client.login(username='testuser', password='testpass123')
        new_label = Label.objects.create(name='Label to Delete')
        response = self.client.post(
            reverse('labels:delete', kwargs={'pk': new_label.pk})
        )
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Label.objects.filter(pk=new_label.pk).exists())
