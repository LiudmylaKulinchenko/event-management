from datetime import datetime
import uuid

from django.db import models
from django.db.models import UniqueConstraint

from event_manager import settings


class EventType(models.Model):
    name = models.CharField(max_length=256)

    class Meta:
        ordering = ["name"]

    def __str__(self) -> str:
        return self.name


class Event(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="users"
    )
    event_type = models.ForeignKey(
        "EventType",
        on_delete=models.CASCADE,
        related_name="event_types"
    )
    info = models.JSONField()
    timestamp = models.DateTimeField()
    created_at = models.DateTimeField(auto_now=True)

    class Meta:
        constraints = [
            UniqueConstraint(
                name="unique_event",
                fields=("user", "event_type")
            )
        ]

    def __str__(self) -> str:
        date = datetime.strftime(self.timestamp, "%H:%M, %m.%d.%Y")

        return f"{self.event_type.name} ({date})"
