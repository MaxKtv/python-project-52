from django.contrib.auth.models import User
from django.test import Client, TestCase
from django.urls import reverse

from task_manager.labels.models import Label
from task_manager.statuses.models import Status
from task_manager.tasks.models import Task


class TasksTest(TestCase):
    fixtures = ['users.json', 'statuses.json', 'labels.json', 'tasks.json']

    def setUp(self):
        self.client = Client()
        # Создаем тестовых пользователей с явным указанием пароля
        self.user1 = User.objects.get(username='testuser1')
        self.user1.set_password('testpass123')
        self.user1.save()

        self.user2 = User.objects.get(username='testuser2')
        self.user2.set_password('testpass123')
        self.user2.save()

        # Получаем существующие объекты из фикстур
        self.status = Status.objects.get(name='New')
        self.label = Label.objects.get(name='Bug')
        self.task = Task.objects.get(name='Fix login bug')

    def test_task_list_authenticated(self):
        """Тест просмотра списка задач авторизованным пользователем."""
        self.client.login(username='testuser1', password='testpass123')
        response = self.client.get(reverse('tasks:list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'tasks/task_list.html')

    def test_task_list_unauthenticated(self):
        """Тест просмотра списка задач неавторизованным пользователем."""
        response = self.client.get(reverse('tasks:list'))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('login'))

    def test_task_create_authenticated(self):
        """Тест создания задачи авторизованным пользователем."""
        self.client.login(username='testuser1', password='testpass123')
        response = self.client.post(reverse('tasks:create'), {
            'name': 'New Task',
            'description': 'New Description',
            'status': self.status.pk,
            'executor': self.user2.pk,
            'labels': [self.label.pk]
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Task.objects.filter(name='New Task').exists())

    def test_task_create_unauthenticated(self):
        """Тест создания задачи неавторизованным пользователем."""
        response = self.client.post(reverse('tasks:create'), {
            'name': 'New Task',
            'description': 'New Description',
            'status': self.status.pk,
            'executor': self.user2.pk
        })
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Task.objects.filter(name='New Task').exists())

    def test_task_update_authenticated(self):
        """Тест обновления задачи авторизованным пользователем."""
        self.client.login(username='testuser1', password='testpass123')
        response = self.client.post(
            reverse('tasks:update', kwargs={'pk': self.task.pk}),
            {
                'name': 'Updated Task',
                'description': 'Updated Description',
                'status': self.status.pk,
                'executor': self.user2.pk,
                'labels': [self.label.pk]
            }
        )
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Task.objects.filter(name='Updated Task').exists())

    def test_task_update_unauthenticated(self):
        """Тест обновления задачи неавторизованным пользователем."""
        response = self.client.post(
            reverse('tasks:update', kwargs={'pk': self.task.pk}),
            {
                'name': 'Updated Task',
                'description': 'Updated Description',
                'status': self.status.pk,
                'executor': self.user2.pk
            }
        )
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Task.objects.filter(name='Updated Task').exists())

    def test_task_delete_by_author(self):
        """Тест удаления задачи ее автором."""
        self.client.login(username='testuser1', password='testpass123')
        response = self.client.post(
            reverse('tasks:delete', kwargs={'pk': self.task.pk})
        )
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Task.objects.filter(pk=self.task.pk).exists())

    def test_task_delete_by_non_author(self):
        """Тест удаления задачи не автором."""
        self.client.login(username='testuser2', password='testpass123')
        response = self.client.post(
            reverse('tasks:delete', kwargs={'pk': self.task.pk})
        )
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Task.objects.filter(pk=self.task.pk).exists())
