from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse


class BaseCRUDTest(TestCase):
    """Базовый класс для тестирования CRUD операций"""

    model = None
    base_url_name = None
    valid_data = {}
    invalid_data = {}

    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="testpass")
        self.client.force_login(self.user)
        self.instance = self.model.objects.create(**self.valid_data)

    def get_url(self, action, args=None):
        """Получает URL для конкретного действия"""
        url_name = (
            self.base_url_name if action == "list" else f"{self.base_url_name}_{action}"
        )
        return reverse(url_name, args=args)

    def get_test_data(self, prefix="test"):
        """Генерирует тестовые данные на основе valid_data"""
        return {k: f"{prefix}_{v}" for k, v in self.valid_data.items()}

    def get_template_path(self, suffix):
        """Возвращает путь к шаблону"""
        return (
            f"{self.model._meta.app_label}/"
            f"{self.model._meta.model_name}_{suffix}.html"
        )

    def assert_view_response(self, response, template_suffix):
        """Проверяет ответ представления"""
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, self.get_template_path(template_suffix))

    def assert_redirect_response(self, response, redirect_url=None):
        """Проверяет ответ с перенаправлением"""
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, redirect_url or self.get_url("list"))

    def test_list_view(self):
        """Тестирование просмотра списка"""
        response = self.client.get(self.get_url("list"))
        self.assert_view_response(response, "list")

    def test_create_view(self):
        """Тестирование отображения формы создания"""
        response = self.client.get(self.get_url("create"))
        self.assert_view_response(response, "form")

    def test_create(self):
        """Тестирование создания объекта"""
        test_data = self.get_test_data("new")
        response = self.client.post(self.get_url("create"), test_data)
        self.assert_redirect_response(response)
        self.assertEqual(self.model.objects.count(), 2)
        new_obj = self.model.objects.exclude(pk=self.instance.pk).first()
        for key, value in test_data.items():
            self.assertEqual(getattr(new_obj, key), value)

    def test_update_view(self):
        """Тестирование отображения формы редактирования"""
        response = self.client.get(self.get_url("update", args=[self.instance.pk]))
        self.assert_view_response(response, "form")

    def test_update(self):
        """Тестирование обновления объекта"""
        test_data = self.get_test_data("updated")
        response = self.client.post(
            self.get_url("update", args=[self.instance.pk]), test_data
        )
        self.assert_redirect_response(response)
        self.instance.refresh_from_db()
        for key, value in test_data.items():
            self.assertEqual(getattr(self.instance, key), value)

    def test_delete_view(self):
        """Тестирование отображения страницы удаления"""
        response = self.client.get(self.get_url("delete", args=[self.instance.pk]))
        self.assert_view_response(response, "confirm_delete")

    def test_delete(self):
        """Тестирование удаления объекта"""
        response = self.client.post(self.get_url("delete", args=[self.instance.pk]))
        self.assert_redirect_response(response)
        self.assertEqual(self.model.objects.count(), 0)

    def test_delete_protected(self):
        """Тестирование защиты от удаления используемого объекта"""
        if not hasattr(self.instance, "task_set"):
            return

        task_model = self.instance.task_set.model
        task_model.objects.create(
            name="Test Task",
            description="Test Description",
            status=self.instance
            if isinstance(
                self.instance, task_model._meta.get_field("status").related_model
            )
            else None,
            executor=self.user,
            author=self.user,
            label=self.instance
            if isinstance(
                self.instance, task_model._meta.get_field("label").related_model
            )
            else None,
        )

        response = self.client.post(self.get_url("delete", args=[self.instance.pk]))
        self.assert_redirect_response(response)
        self.assertEqual(self.model.objects.count(), 1)
        messages = list(response.wsgi_request._messages)
        self.assertEqual(len(messages), 1)
        self.assertEqual(messages[0].tags, "danger")

    def test_unauthorized_access(self):
        """Тестирование доступа неавторизованного пользователя"""
        self.client.logout()
        urls = [
            ("list", None),
            ("create", None),
            ("update", [self.instance.pk]),
            ("delete", [self.instance.pk]),
        ]
        for action, args in urls:
            response = self.client.get(self.get_url(action, args))
            self.assertEqual(response.status_code, 302)
            self.assertRedirects(response, f"/login/?next={self.get_url(action, args)}")
