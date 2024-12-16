from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User


class BaseCRUDTest(TestCase):
    model = None
    base_url_name = None
    valid_data = None

    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='password'
        )
        self.client.login(username='testuser', password='password')
        self.instance = self.model.objects.create(**self.valid_data)

    def get_url_name(self, action):
        """Получает имя URL для конкретного действия"""
        if action == 'list':
            return self.base_url_name
        return f'{self.base_url_name}_{action}'

    def test_create(self):
        """Тестирование создания объекта"""
        response = self.client.post(
            reverse(self.get_url_name('create')),
            self.valid_data
        )
        self.assertEqual(response.status_code, 302)
        self.assertEqual(self.model.objects.count(), 2)

    def test_update(self):
        """Тестирование обновления объекта"""
        new_data = self.valid_data.copy()
        new_data['name'] = 'Updated'
        response = self.client.post(
            reverse(self.get_url_name('update'), args=[self.instance.pk]),
            new_data
        )
        self.assertEqual(response.status_code, 302)
        self.instance.refresh_from_db()
        self.assertEqual(self.instance.name, 'Updated')

    def test_delete(self):
        """Тестирование удаления объекта"""
        response = self.client.post(
            reverse(self.get_url_name('delete'), args=[self.instance.pk])
        )
        self.assertEqual(response.status_code, 302)
        self.assertEqual(self.model.objects.count(), 0)
