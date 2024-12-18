from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from task_manager.base_tests import BaseCRUDTest
from task_manager.tasks.models import Label, Status, Task


class TaskCRUDTest(BaseCRUDTest):
    model = Task
    base_url_name = 'task'

    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='password'
        )
        self.client.login(username='testuser', password='password')
        self.status = Status.objects.create(name='Новый')
        self.valid_data = {
            'name': 'Задача 1',
            'description': 'Описание',
            'status': self.status.id,
            'author': self.user,
        }
        self.instance = self.model.objects.create(**self.valid_data)

    def test_delete_task_by_non_author(self):
        User.objects.create_user(
            username='another',
            password='password'
        )
        self.client.login(username='another', password='password')
        response = self.client.post(
            reverse(f'{self.base_url_name}_delete', args=[self.instance.pk])
        )
        self.assertEqual(response.status_code, 403)
        self.assertEqual(self.model.objects.count(), 1)


class TaskFilterTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='password'
        )
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
