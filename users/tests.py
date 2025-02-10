from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from users.models import ModelUser


class TrackerTestCase(APITestCase):

    def setUp(self):
        pass

    def test_user_create(self):
        """Тест создания пользователя"""
        data = {"username": "Test", "email": "test@test.ru", "password": "1234", "tg_chat_id": "1234567890"}
        url = reverse("users:register")
        response = self.client.post(url, data=data)
        data = response.json()

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        self.assertEqual(data.get("username"), "Test")

        self.assertTrue(ModelUser.objects.all().exists())

    def test_get_user(self):
        """Тест вывода пользователя"""

        user = ModelUser.objects.create(username="Test", email="test@test.ru")
        self.client.force_authenticate(user=user)
        url = reverse("users:user_get", args=(user.pk,))
        response = self.client.get(url)
        data = response.json()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data.get("email"), "test@test.ru")
