from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from event.models import EventType, User, Event


class EventAdmin(admin.ModelAdmin):
    list_display = ["user", "event_type", "info", "timestamp", "created_at"]
    list_filter = ["event_type", "timestamp"]


admin.site.register(EventType)
admin.site.register(Event, EventAdmin)
admin.site.register(User, UserAdmin)
