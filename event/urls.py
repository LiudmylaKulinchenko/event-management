from django.urls import path

from event.views import EventTypeView, EventView


urlpatterns = [
    path("events/", EventView.as_view(), name="event-list"),
    path("event-types/", EventTypeView.as_view(), name="event-type-list"),
]

app_name = "event"
