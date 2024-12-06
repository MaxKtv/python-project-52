from django.urls import reverse
from django.contrib.auth.models import User
from task_manager.base_tests import BaseCRUDTest
from task_manager.labels.models import Label


class LabelCRUDTest(BaseCRUDTest):
    model = Label
    base_url_name = 'labels'
    valid_data = {'name': 'Bug'}

    def setUp(self):
        self.user = User.objects.create_user(username='testuser',
                                             password='password')
        self.client.login(username='testuser', password='password')
        self.label = Label.objects.create(name='Bug')

    def test_create_label(self):
        self.client.post(reverse('labels_create'), {'name': 'Feature'})
        self.assertEqual(Label.objects.count(), 2)

    def test_update_label(self):
        self.client.post(
            reverse('labels_update', args=[self.label.pk]),
            {'name': 'Fix'}
        )
        self.label.refresh_from_db()
        self.assertEqual(self.label.name, 'Fix')

    def test_delete_label_protected(self):
        self.client.post(reverse('labels_delete', args=[self.label.pk]))
        self.assertEqual(Label.objects.count(), 1)
