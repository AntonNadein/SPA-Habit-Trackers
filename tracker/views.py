from rest_framework import generics, viewsets
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from tracker.models import TrackerModel
from tracker.pagination import TrackerPagination
from tracker.serializers import TrackerModelSerializer
from tracker.tasks import get_setting_tracker
from users.permissions import IsOwner


class TrackerModelViewSet(viewsets.ModelViewSet):
    """CRUD для модели привычки конкретного пользователя"""

    serializer_class = TrackerModelSerializer
    pagination_class = TrackerPagination
    permission_classes = [
        IsOwner,
    ]

    def get_queryset(self):
        """Получение queryset пустой для документации и отфильтрованный для пользователей"""
        if "redoc" in self.request.path or "swagger" in self.request.path:
            return TrackerModel.objects.none()
        else:
            user = self.request.user
            return TrackerModel.objects.filter(owner=user)

    def perform_create(self, serializer):
        """Добавление новому пользователю защищенного пароля и отложенной задачи для телеграмм бота"""
        tracker = serializer.save()
        user = self.request.user
        tracker.owner = user
        tracker.save()
        # создаем отложенную задачу в телеграмм
        if user.tg_chat_id:
            get_setting_tracker(tracker.time, tracker.periodicity, str(tracker), str(user.tg_chat_id))


class TrackerModelGenericList(generics.ListAPIView):
    """Список публичных привычек"""

    serializer_class = TrackerModelSerializer
    permission_classes = [
        IsAuthenticatedOrReadOnly,
    ]
    pagination_class = TrackerPagination

    def get_queryset(self):
        return TrackerModel.objects.filter(is_public=True)
