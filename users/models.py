from django.contrib.auth.models import AbstractUser
from django.db import models


class ModelUser(AbstractUser):
    """Модель пользователь"""

    email = models.EmailField(unique=True, verbose_name="Email-адрес", help_text="Введите свой Email-адрес")

    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = [
        "email",
    ]

    def __str__(self):
        return f"{self.username} с адресом: {self.email}"

    class Meta:
        verbose_name = "пользователь"
        verbose_name_plural = "Пользователи"
