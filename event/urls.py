from django.urls import path, include
from rest_framework import routers

from event.views import EventTypeView, EventView


urlpatterns = [
    path("events/", EventView.as_view(), name="list-event"),
    path("event-types/", EventTypeView.as_view(), name="list-event-type"),
]

app_name = "event"
