from django.db import models
from django.db.models import CASCADE

from users.models import ModelUser


class TrackerModel(models.Model):
    owner = models.ForeignKey(
        ModelUser,
        on_delete=CASCADE,
        related_name="user",
        null=True,
        blank=True,
        verbose_name="Пользователь",
        help_text="ID пользователя",
    )
    locations = models.CharField(
        max_length=255, verbose_name="Место", help_text="Введите где хотите выполнять действие"
    )
    time = models.TimeField(verbose_name="Время выполнения", help_text="Введите во сколько хотите выполнять действие")
    action = models.CharField(
        max_length=255,
        verbose_name="Действие/привычка",
        help_text="Введите действие из котрого хотите сформировать привычку",
    )
    is_nice = models.BooleanField(
        verbose_name="Признак приятной привычки", help_text="Отметьте, если привычка приятная"
    )
    associated_habit = models.ForeignKey(
        "self",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="habit",
        verbose_name="Связанная привычка",
        help_text="Выберете привычку из приятных",
    )
    periodicity = models.PositiveSmallIntegerField(
        verbose_name="Периодичность", help_text="Периодичность выполнения действия"
    )
    reward = models.CharField(
        max_length=255,
        null=True,
        blank=True,
        verbose_name="Вознаграждение",
        help_text="Вознаграждение за выполнение действия",
    )
    time_to_complete = models.PositiveSmallIntegerField(
        verbose_name="Время на выполнение", help_text="Максимальное время на выполнение 120 секунд"
    )
    is_public = models.BooleanField(verbose_name="Признак публичности", help_text="Отметка, для общего пользования")

    def __str__(self):
        return f"Я буду {self.action} в {self.time} в {self.locations}"

    class Meta:
        verbose_name = "Трекер привычек"
        verbose_name_plural = "Трекер привычек"
