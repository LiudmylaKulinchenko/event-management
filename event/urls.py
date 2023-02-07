from django.urls import path, include
from rest_framework import routers

from event.views import EventTypeViewSet, EventViewSet

router = routers.DefaultRouter()
router.register("event-types", EventTypeViewSet)
router.register("events", EventViewSet)

urlpatterns = [path("", include(router.urls))]

app_name = "event"
