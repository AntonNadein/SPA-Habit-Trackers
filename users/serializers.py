from rest_framework import serializers

from users.models import ModelUser


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = ModelUser
        fields = ("username", "password", "email", "first_name", "last_name", "tg_chat_id")
