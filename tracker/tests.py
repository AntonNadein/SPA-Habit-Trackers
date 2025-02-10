from django.urls import reverse
from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.test import APITestCase

from tracker.models import TrackerModel
from users.models import ModelUser


class TrackerTestCase(APITestCase):

    def setUp(self):
        self.user = ModelUser.objects.create(username="Testov", email="test@test.ru")
        self.tracker = TrackerModel.objects.create(
            owner=self.user,
            locations="Кухня",
            time="19:30",
            action="Съесть конфету",
            is_nice=True,
            periodicity=1,
            time_to_complete=100,
            is_public=True,
        )
        self.client.force_authenticate(user=self.user)

    def test_tracker_retrieve(self):
        """Тест получения задачи"""
        url = reverse("tracker:tracker-detail", args=(self.tracker.pk,))
        response = self.client.get(url)
        data = response.json()
        status_code_tracker = response.status_code
        self.assertEqual(status_code_tracker, status.HTTP_200_OK)
        self.assertEqual(data.get("action"), self.tracker.action)

    def test_tracker_create(self):
        """Тест создания задачи"""
        url = reverse("tracker:tracker-list")
        data = {
            "locations": "Кухня",
            "time": "19:30",
            "action": "поесть",
            "is_nice": False,
            "periodicity": 1,
            "time_to_complete": 100,
            "is_public": True,
            "reward": "Попить воды",
        }
        response = self.client.post(url, data)
        status_code_tracker = response.status_code
        self.assertEqual(status_code_tracker, status.HTTP_201_CREATED)
        self.assertEqual(TrackerModel.objects.all().count(), 2)
        data_2 = {
            "locations": "Зал",
            "time": "19:30",
            "action": "Приседать",
            "is_nice": False,
            "periodicity": 1,
            "time_to_complete": 60,
            "is_public": True,
            "associated_habit": 1,
        }
        self.client.post(url, data_2)
        self.assertEqual(TrackerModel.objects.all().count(), 3)
        self.assertEqual(data_2.get("associated_habit"), 1)

    def test_tracker_create_validation(self):
        """Тест валидатора создания задачи"""
        url = reverse("tracker:tracker-list")
        # тест продолжительности
        data = {
            "locations": "Кухня",
            "time": "17:30",
            "action": "поесть",
            "is_nice": False,
            "periodicity": 1,
            "time_to_complete": 140,
            "is_public": True,
            "reward": "Попить воды",
        }
        response = self.client.post(url, data)
        status_code_lesson = response.status_code
        self.assertEqual(status_code_lesson, status.HTTP_400_BAD_REQUEST)
        self.assertRaises(ValidationError)

        data["time_to_complete"] = -1
        response = self.client.post(url, data)
        status_code_lesson = response.status_code
        self.assertEqual(status_code_lesson, status.HTTP_400_BAD_REQUEST)
        self.assertRaises(ValidationError)

        # тест периодичности
        data["time_to_complete"] = 60
        data["periodicity"] = -1
        response = self.client.post(url, data)
        status_code_lesson = response.status_code
        self.assertEqual(status_code_lesson, status.HTTP_400_BAD_REQUEST)
        self.assertRaises(ValidationError)

        data["periodicity"] = 8
        response = self.client.post(url, data)
        status_code_lesson = response.status_code
        self.assertEqual(status_code_lesson, status.HTTP_400_BAD_REQUEST)
        self.assertRaises(ValidationError)

        # тест правильной работы
        data["time_to_complete"] = 60
        data["periodicity"] = 5
        response = self.client.post(url, data)
        status_code_lesson = response.status_code
        data = response.json()
        self.assertEqual(status_code_lesson, status.HTTP_201_CREATED)
        self.assertEqual(data.get("periodicity"), 5)
        self.assertEqual(data.get("time_to_complete"), 60)

    def test_tracker_update(self):
        """Тест обновления задачи"""
        url = reverse("tracker:tracker-detail", args=(self.tracker.pk,))
        data = {"is_public": False}
        response = self.client.patch(url, data)
        data = response.json()
        status_code_lesson = response.status_code
        self.assertEqual(status_code_lesson, status.HTTP_200_OK)
        self.assertEqual(data.get("is_public"), False)

    def test_tracker_update_validation(self):
        """Тест валидатора обновления задач"""
        url = reverse("tracker:tracker-detail", args=(self.tracker.pk,))
        url_2 = reverse("tracker:tracker-list")
        data = {
            "locations": "Кухня",
            "time": "19:30",
            "action": "поесть",
            "is_nice": True,
            "periodicity": 1,
            "time_to_complete": 100,
            "is_public": True,
        }
        response_2 = self.client.post(url_2, data)

        # У приятной привычки не может быть вознаграждения
        data = {"reward": "Попить воды"}
        response = self.client.patch(url, data)
        status_code_lesson = response.status_code
        self.assertEqual(status_code_lesson, status.HTTP_400_BAD_REQUEST)
        self.assertRaises(ValidationError)

        # У приятной привычки не может быть связанной привычки.
        url_3 = reverse("tracker:tracker-detail", args=(response_2.json().get("id"),))
        data = {"associated_habit": self.tracker.pk}
        response = self.client.patch(url_3, data)
        status_code_lesson = response.status_code
        self.assertEqual(status_code_lesson, status.HTTP_400_BAD_REQUEST)
        self.assertRaises(ValidationError)

        # Невозможен одновременный выбор связанной привычки и указания вознаграждения.
        data = {"is_nice": False, "reward": "Попить воды"}
        self.client.patch(url, data)
        data = {"associated_habit": response_2.json().get("id")}
        response_3 = self.client.patch(url, data)
        status_code_lesson = response_3.status_code
        self.assertEqual(status_code_lesson, status.HTTP_400_BAD_REQUEST)
        self.assertRaises(ValidationError)

        # В связанные привычки могут попадать только привычки с признаком приятной привычки. is_nice=True
        data = {"reward": ""}
        self.client.patch(url, data)
        data = {
            "locations": "Кухня",
            "time": "19:30",
            "action": "поесть",
            "is_nice": False,
            "periodicity": 1,
            "time_to_complete": 100,
            "is_public": True,
            "associated_habit": self.tracker.pk,
        }
        response_2 = self.client.post(url_2, data)
        status_code_lesson = response_2.status_code
        self.assertEqual(status_code_lesson, status.HTTP_400_BAD_REQUEST)
        self.assertRaises(ValidationError)

        # Вы не являетесь владельцем модели.
        user_2 = ModelUser.objects.create(username="Testov_2", email="test_2@test.ru")
        tracker_2 = TrackerModel.objects.create(
            owner=user_2,
            locations="Кухня",
            time="19:30",
            action="Съесть конфету",
            is_nice=True,
            periodicity=1,
            time_to_complete=100,
            is_public=True,
        )
        data = {"associated_habit": tracker_2.pk}
        response = self.client.patch(url, data)
        status_code_lesson = response.status_code
        self.assertEqual(status_code_lesson, status.HTTP_400_BAD_REQUEST)
        self.assertRaises(ValidationError)

    def test_tracker_delete(self):
        """Тест удаления задачи"""
        url = reverse("tracker:tracker-detail", args=(self.tracker.pk,))
        response = self.client.delete(url)
        status_code_lesson = response.status_code
        self.assertEqual(status_code_lesson, status.HTTP_204_NO_CONTENT)
        self.assertEqual(TrackerModel.objects.all().count(), 0)

    def test_tracker_list(self):
        """Тест вывода списка задач"""
        url = reverse("tracker:tracker-list")
        response = self.client.get(url)
        status_code_lesson = response.status_code
        data = response.json()
        self.assertEqual(status_code_lesson, status.HTTP_200_OK)
        result = {
            "count": 1,
            "next": None,
            "previous": None,
            "results": [
                {
                    "id": self.tracker.pk,
                    "time_to_complete": self.tracker.time_to_complete,
                    "periodicity": self.tracker.periodicity,
                    "locations": self.tracker.locations,
                    "time": "19:30:00",
                    "action": self.tracker.action,
                    "is_nice": self.tracker.is_nice,
                    "reward": None,
                    "is_public": self.tracker.is_public,
                    "owner": self.user.pk,
                    "associated_habit": None,
                }
            ],
        }
        self.assertEqual(data, result)

    def test_tracker_public_list(self):
        """Тест вывода списка опубликованных задач"""
        user_2 = ModelUser.objects.create(username="Testov_2", email="test_2@test.ru")
        TrackerModel.objects.create(
            owner=user_2,
            locations="Кухня",
            time="19:30",
            action="Съесть конфету",
            is_nice=True,
            periodicity=1,
            time_to_complete=100,
            is_public=True,
        )
        TrackerModel.objects.create(
            owner=user_2,
            locations="Кухня",
            time="19:30",
            action="Съесть конфету",
            is_nice=True,
            periodicity=1,
            time_to_complete=100,
            is_public=False,
        )

        url = reverse("tracker:tracker_public")
        response = self.client.get(url)
        status_code_lesson = response.status_code
        data = response.json()
        self.assertEqual(status_code_lesson, status.HTTP_200_OK)
        self.assertEqual(data.get("count"), 2)
