from django.contrib import admin

from event.models import EventType, Event


class EventAdmin(admin.ModelAdmin):
    list_display = ["user", "event_type", "info", "timestamp", "created_at"]
    list_filter = ["event_type", "timestamp"]


admin.site.register(EventType)
admin.site.register(Event, EventAdmin)
