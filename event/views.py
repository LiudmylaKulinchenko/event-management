from rest_framework import viewsets

from event.models import EventType, Event
from event.serializers import EventTypeSerializer, EventSerializer


class EventTypeViewSet(viewsets.ModelViewSet):
    queryset = EventType.objects.all()
    serializer_class = EventTypeSerializer


class EventViewSet(viewsets.ModelViewSet):
    queryset = Event.objects.all()
    serializer_class = EventSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
