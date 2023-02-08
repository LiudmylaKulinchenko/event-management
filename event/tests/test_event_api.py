from datetime import datetime
import json

import pytz
from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from event.models import EventType, Event
from event.serializers import EventTypeSerializer, EventSerializer
from event_manager.settings import TIME_ZONE

EVENT_TYPES_URL = reverse("event:event-type-list")
EVENTS_URL = reverse("event:event-list")


def create_user(**params):
    return get_user_model().objects.create_user(**params)


def sample_event_type(**params) -> EventType:
    defaults = {"name": "Sample event type"}
    defaults.update(params)

    return EventType.objects.create(**defaults)


def sample_event(user: get_user_model(), **params) -> Event:
    client = APIClient()
    client.force_authenticate(user)

    sample_info = json.dumps(
        {
            "price": 10,
            "place": "Test",
        }
    )

    defaults = {
        "user": user,
        "event_type": "Sample event type",
        "info": sample_info,
        "timestamp": datetime.now()
    }
    defaults.update(params)

    return client.post(EVENTS_URL, **defaults)


class UnauthenticatedEventApiTests(TestCase):
    def setUp(self) -> None:
        self.client = APIClient()

    def test_event_types_list(self):
        sample_event_type()
        sample_event_type(name="Test event type")

        res = self.client.get(EVENT_TYPES_URL)
        event_types = EventType.objects.all()
        serializer = EventTypeSerializer(event_types, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_events_list(self):
        user = create_user(email="test@test.com", password="test12345")
        sample_event(user=user, info=None)
        sample_event(user=user, event_type="Test event type")

        res = self.client.get(EVENTS_URL)
        event_types = Event.objects.all()
        serializer = EventSerializer(event_types, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)


class AuthenticatedEventApiTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            "test@test.com",
            "test12345"
        )
        self.client.force_authenticate(self.user)

    def test_create_event_type(self):
        payload = {"name": "Test event type"}

        res = self.client.post(EVENT_TYPES_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

        event_type = EventType.objects.get(id=res.data["id"])
        self.assertEqual(payload["name"], getattr(event_type, "name"))

    def test_create_event_with_existing_event_type(self):
        event_type = sample_event_type()

        payload = {
            "event_type": event_type,
            "timestamp": datetime.now(pytz.timezone(TIME_ZONE))
        }

        res = self.client.post(EVENTS_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

        event_type = Event.objects.get(id=res.data["id"])
        for key in payload:
            self.assertEqual(payload[key], getattr(event_type, key))

    def test_create_event_with_new_event_type(self):
        event_type_name = "New event type"
        payload = {
            "event_type": event_type_name,
            "timestamp": datetime.now(pytz.timezone(TIME_ZONE))
        }

        res = self.client.post(EVENTS_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

        try:
            event_type = EventType.objects.get(name=event_type_name)
        except EventType.DoesNotExist:
            event_type = None

        self.assertTrue(event_type)
        self.assertEqual(event_type.name, event_type_name)
