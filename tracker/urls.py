from django.urls import path
from rest_framework.routers import DefaultRouter

from tracker.apps import TrackerConfig
from tracker.views import TrackerModelGenericList, TrackerModelViewSet

app_name = TrackerConfig.name

router = DefaultRouter()
router.register(r"tracker", TrackerModelViewSet, basename="tracker")

urlpatterns = [
    path("tracker/public/", TrackerModelGenericList.as_view(), name="tracker_public"),
] + router.urls
