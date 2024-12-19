from django.contrib.auth.models import User

from task_manager.base import BaseCRUDTest


class UserCRUDTest(BaseCRUDTest):
    model = User
    base_url_name = "user"
    valid_data = {
        "username": "testuser2",
        "password1": "testpass123",
        "password2": "testpass123",
        "first_name": "Test",
        "last_name": "User",
    }

    def test_unauthorized_update(self):
        """Тест запрета редактирования другого пользователя"""
        other_user = User.objects.create_user(
            username="other", password="testpass"
        )
        response = self.client.post(
            self.get_url("update", args=[other_user.pk]),
            {"username": "changed"},
        )
        self.assertEqual(response.status_code, 403)
        other_user.refresh_from_db()
        self.assertEqual(other_user.username, "other")

    def test_unauthorized_delete(self):
        """Тест запрета удаления другого пользователя"""
        other_user = User.objects.create_user(
            username="other", password="testpass"
        )
        response = self.client.post(
            self.get_url("delete", args=[other_user.pk])
        )
        self.assertEqual(response.status_code, 403)
        self.assertTrue(User.objects.filter(username="other").exists())
