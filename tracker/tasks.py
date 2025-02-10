import json

import requests
from celery import shared_task
from django_celery_beat.models import CrontabSchedule, PeriodicTask

from config import settings


def get_setting_tracker(times, day, text, chat_id):
    """Настройка добавления отложенной задачи Celery"""
    # Создаем интервал для повтора
    schedule, created = CrontabSchedule.objects.get_or_create(
        minute=str(times.minute),
        hour=str(times.hour),
        day_of_week=str(day),
        day_of_month="*",
        month_of_year="*",
    )

    # Создаем задачу для повторения
    PeriodicTask.objects.create(
        crontab=schedule,
        name=text,
        task="tracker.tasks.send_tg_chat_message",
        args=json.dumps([text, chat_id]),
    )


@shared_task
def send_tg_chat_message(text, chat_id):
    """Функция отправки сообщения в телеграмм бот"""
    params = {
        "text": text,
        "chat_id": chat_id,
    }
    requests.get(f"{settings.TG_BOT_URL}{settings.TG_BOT_TOKEN}/sendMessage", params=params)
