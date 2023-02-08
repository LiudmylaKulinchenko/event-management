from django.db import transaction
from rest_framework import serializers

from event.models import EventType, Event


class EventTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = EventType
        fields = ("id", "name")


class EventSerializer(serializers.ModelSerializer):
    user = serializers.CharField(source="user.email", read_only=True)
    event_type = serializers.CharField(source="event_type.name")

    class Meta:
        model = Event
        fields = (
            "id",
            "user",
            "event_type",
            "info",
            "timestamp",
            "created_at",
        )

    def create(self, validated_data):
        with transaction.atomic():
            event_type_name = validated_data.pop("event_type")["name"]
            event_type = EventType.objects.get_or_create(
                name=event_type_name
            )[0]
            event = Event.objects.create(
                event_type=event_type, **validated_data
            )

            return event
