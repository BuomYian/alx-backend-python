"""
Django admin configuration for the messaging app.
"""
from django.contrib import admin
from .models import EventLog, Message


@admin.register(EventLog)
class EventLogAdmin(admin.ModelAdmin):
    """Admin interface for EventLog model."""
    list_display = ('event_type', 'related_user', 'created_at')
    list_filter = ('event_type', 'created_at')
    search_fields = ('description', 'related_user__username')
    readonly_fields = ('created_at', 'updated_at')
    ordering = ('-created_at',)


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    """Admin interface for Message model."""
    list_display = ('sender', 'recipient', 'subject', 'is_read', 'created_at')
    list_filter = ('is_read', 'created_at')
    search_fields = ('subject', 'content', 'sender__username',
                     'recipient__username')
    readonly_fields = ('created_at', 'updated_at')
    ordering = ('-created_at',)
