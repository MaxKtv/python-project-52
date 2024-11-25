from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from task_manager.labels.models import Label


class LabelCRUDTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='password')
        self.client.login(username='testuser', password='password')
        self.label = Label.objects.create(name='Bug')

    def test_create_label(self):
        response = self.client.post(reverse('label_create'), {'name': 'Feature'})
        self.assertEqual(Label.objects.count(), 2)

    def test_update_label(self):
        response = self.client.post(reverse('label_update', args=[self.label.pk]), {'name': 'Fix'})
        self.label.refresh_from_db()
        self.assertEqual(self.label.name, 'Fix')

    def test_delete_label_protected(self):
        response = self.client.post(reverse('label_delete', args=[self.label.pk]))
        self.assertEqual(Label.objects.count(), 1)
