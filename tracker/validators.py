from rest_framework.serializers import ValidationError


class TimeToCompleteValidator:
    """Валидатор времени выполнения"""

    def __init__(self, field):
        self.field = field

    def __call__(self, value):
        if isinstance(value, int) and (0 <= value <= 120):
            return  # Значение корректное, ничего не делать
        raise ValidationError("Время на выполнение должно быть целым числом от 0 до 120 секунд")


class PeriodicityValidator:
    """Валидатор периодичности выполнения"""

    def __init__(self, field):
        self.field = field

    def __call__(self, value):
        if isinstance(value, int) and (0 < value <= 7):
            return  # Значение корректное, ничего не делать
        raise ValidationError("Нельзя выполнять привычку реже, чем 1 раз в 7 дней")


def validation_data(is_nice, reward, associated_habit, request_data):
    """Валидатор для общей валидации"""
    if is_nice and reward:
        raise ValidationError("У приятной привычки не может быть вознаграждения.")
    elif is_nice and associated_habit:
        raise ValidationError("У приятной привычки не может быть связанной привычки.")
    elif reward and associated_habit:
        raise ValidationError("Невозможен одновременный выбор связанной привычки и указания вознаграждения.")
    elif associated_habit and not associated_habit.is_nice:
        raise ValidationError(
            "В связанные привычки могут попадать только привычки с признаком приятной привычки. is_nice=True"
        )
    elif associated_habit and associated_habit.is_nice:
        if request_data.user != associated_habit.owner:
            raise ValidationError(f"Вы не являетесь владельцем модели {associated_habit}")
