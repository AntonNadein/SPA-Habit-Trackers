from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from users.models import ModelUser
from users.serializers import UserSerializer


class UsersCreateAPIview(generics.CreateAPIView):
    serializer_class = UserSerializer
    queryset = ModelUser.objects.all()

    def perform_create(self, serializer):
        """Создаем пользователя с защищенным паролем"""
        user = serializer.save(is_active=True)
        user.set_password(user.password)
        user.save()


class UsersDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    """Получение, изменение, удаление пользователя"""
    serializer_class = UserSerializer
    queryset = ModelUser.objects.all()
    permission_classes = [IsAuthenticated]
