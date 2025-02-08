from rest_framework import generics, viewsets
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from tracker.models import TrackerModel
from tracker.pagination import TrackerPagination
from tracker.serializers import TrackerModelSerializer
from users.permissions import IsOwner


class TrackerModelViewSet(viewsets.ModelViewSet):
    """CRUD для модели привычки конкретного пользователя"""

    serializer_class = TrackerModelSerializer
    pagination_class = TrackerPagination
    permission_classes = [
        IsOwner,
    ]

    def get_queryset(self):
        user = self.request.user
        return TrackerModel.objects.filter(owner=user)

    def perform_create(self, serializer):
        tracker = serializer.save()
        tracker.owner = self.request.user
        tracker.save()

    # def get_permissions(self):
    #     if self.action in ["create", "retrieve", "update", "destroy"]:
    #         self.permission_classes = (IsOwner,)
    #     elif self.action == "list":
    #         self.permission_classes = (IsAuthenticatedOrReadOnly,)
    #     return super().get_permissions()


class TrackerModelGenericList(generics.ListAPIView):
    """Список публичных привычек"""

    serializer_class = TrackerModelSerializer
    permission_classes = [
        IsAuthenticatedOrReadOnly,
    ]
    pagination_class = TrackerPagination

    def get_queryset(self):
        return TrackerModel.objects.filter(is_public=True)
