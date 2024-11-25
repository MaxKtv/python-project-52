from django.test import TestCase
from django.urls import reverse
from .models import Status
from django.contrib.auth.models import User


class StatusCRUDTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='password')
        self.client.login(username='testuser', password='password')
        self.status = Status.objects.create(name='Новый')

    def test_create_status(self):
        response = self.client.post(reverse('status_create'), {'name': 'В работе'})
        self.assertEqual(Status.objects.count(), 2)

    def test_update_status(self):
        response = self.client.post(reverse('status_update', args=[self.status.pk]), {'name': 'Изменен'})
        self.status.refresh_from_db()
        self.assertEqual(self.status.name, 'Изменен')

    def test_delete_status(self):
        response = self.client.post(reverse('status_delete', args=[self.status.pk]))
        self.assertEqual(Status.objects.count(), 0)