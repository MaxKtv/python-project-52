from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from task_manager.tasks.models import Task, Status, Label


class TaskCRUDTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser',
                                             password='password')
        self.client.login(username='testuser', password='password')
        self.status = Status.objects.create(name='Новый')
        self.task = Task.objects.create(
            name='Задача 1',
            description='Описание',
            status=self.status,
            author=self.user,
        )

    def test_create_task(self):
        self.client.post(reverse('task_create'), {
            'name': 'Задача 2',
            'description': 'Описание задачи',
            'status': self.status.id,
        })
        self.assertEqual(Task.objects.count(), 2)

    def test_update_task(self):
        self.client.post(reverse('task_update', args=[self.task.id]), {
            'name': 'Обновленная задача',
            'description': 'Новое описание',
            'status': self.status.id,
        })
        self.task.refresh_from_db()
        self.assertEqual(self.task.name, 'Обновленная задача')

    def test_delete_task_by_author(self):
        self.client.post(reverse('task_delete', args=[self.task.id]))
        self.assertEqual(Task.objects.count(), 0)

    def test_delete_task_by_non_author(self):
        User.objects.create_user(username='another', password='password')
        self.client.login(username='another', password='password')
        response = self.client.post(reverse('task_delete', args=[self.task.id]))
        self.assertEqual(response.status_code, 403)
        self.assertEqual(Task.objects.count(), 1)


class TaskFilterTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser',
                                             password='password')
        self.client.login(username='testuser', password='password')
        self.status = Status.objects.create(name='Новый')
        self.label = Label.objects.create(name='Bug')
        self.task1 = Task.objects.create(
            name='Task 1',
            description='Description 1',
            status=self.status,
            author=self.user,
        )
        self.task1.labels.add(self.label)

    def test_filter_by_status(self):
        response = self.client.get(reverse('tasks'), {'status': self.status.id})
        self.assertContains(response, 'Task 1')

    def test_filter_self_tasks(self):
        response = self.client.get(reverse('tasks'), {'self_tasks': 'on'})
        self.assertContains(response, 'Task 1')
