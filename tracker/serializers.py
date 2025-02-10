from rest_framework import serializers

from tracker.models import TrackerModel
from tracker.validators import PeriodicityValidator, TimeToCompleteValidator, validation_data


class TrackerModelSerializer(serializers.ModelSerializer):
    time_to_complete = serializers.IntegerField(
        required=False, validators=[TimeToCompleteValidator(field="time_to_complete")]
    )
    periodicity = serializers.IntegerField(required=False, validators=[PeriodicityValidator(field="periodicity")])
    reward = serializers.CharField(allow_null=True, required=False)

    class Meta:
        model = TrackerModel
        fields = "__all__"

    def validate(self, attrs):
        """Общая валидация привычек"""
        request_data = self.context.get("request")

        # валидация при создании
        is_nice = attrs.get("is_nice")
        reward = attrs.get("reward")
        associated_habit = attrs.get("associated_habit")

        # валидация в методе PATCH если изменяется один атрибут
        if self.instance:
            is_nice = attrs.get("is_nice", self.instance.is_nice)
            reward = attrs.get("reward", self.instance.reward)
            associated_habit = attrs.get("associated_habit", self.instance.associated_habit)
        validation_data(is_nice, reward, associated_habit, request_data)
        return attrs
