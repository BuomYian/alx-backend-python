"""
Django admin configuration for the messaging app.
"""
from django.contrib import admin
from .models import EventLog, Message


@admin.register(EventLog)
class EventLogAdmin(admin.ModelAdmin):
    """Admin interface for EventLog model."""
    list_display = ('event_type', 'related_user', 'timestamp')
    list_filter = ('event_type', 'timestamp')
    search_fields = ('description', 'related_user__username')
    readonly_fields = ('timestamp', 'updated_at')
    ordering = ('-timestamp',)


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    """Admin interface for Message model."""
    list_display = ('sender', 'receiver', 'subject', 'is_read', 'timestamp')
    list_filter = ('is_read', 'timestamp')
    search_fields = ('subject', 'content', 'sender__username',
                     'receiver__username')
    readonly_fields = ('timestamp', 'updated_at')
    ordering = ('-timestamp',)
