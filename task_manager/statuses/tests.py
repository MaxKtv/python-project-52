from django.urls import reverse
from task_manager.statuses.models import Status
from django.contrib.auth.models import User
from task_manager.base_tests import BaseCRUDTest


class StatusCRUDTest(BaseCRUDTest):
    model = Status
    base_url_name = 'statuses'
    valid_data = {'name': 'Новый'}

    def setUp(self):
        self.user = User.objects.create_user(username='testuser',
                                             password='password')
        self.client.login(username='testuser', password='password')
        self.status = Status.objects.create(name='Новый')

    def test_create_status(self):
        self.client.post(reverse('statuses_create'), {'name': 'В работе'})
        self.assertEqual(Status.objects.count(), 2)

    def test_update_status(self):
        self.client.post(reverse('statuses_update',
                                 args=[self.status.pk]), {'name': 'Изменен'})
        self.status.refresh_from_db()
        self.assertEqual(self.status.name, 'Изменен')

    def test_delete_status(self):
        self.client.post(reverse('statuses_delete', args=[self.status.pk]))
        self.assertEqual(Status.objects.count(), 0)
