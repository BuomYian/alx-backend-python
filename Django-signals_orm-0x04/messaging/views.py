"""
Views for the messaging app.
Demonstrates efficient ORM queries and caching strategies.
"""
from django.shortcuts import render
from django.core.cache import cache
from django.views.decorators.cache import cache_page
from .models import EventLog, Message


def event_log_list(request):
    """
    Display event logs with query optimization.
    Uses select_related and caching for performance.
    """
    # Try to get from cache first
    cache_key = 'event_logs_list'
    logs = cache.get(cache_key)

    if logs is None:
        # Query with optimization - select_related for User
        logs = EventLog.objects.select_related('related_user').all()[:100]
        # Cache for 5 minutes
        cache.set(cache_key, logs, 300)

    return render(request, 'messaging/event_logs.html', {'logs': logs})


@cache_page(60 * 5)  # Cache view for 5 minutes
def message_list(request):
    """
    Display messages with view-level caching.
    Demonstrates efficient prefetch_related usage.
    """
    if request.user.is_authenticated:
        # Optimize with prefetch_related for reverse FK
        messages = Message.objects.filter(
            receiver=request.user
        ).select_related('sender').order_by('-timestamp')[:50]
    else:
        messages = []

    return render(request, 'messaging/messages.html', {'messages': messages})
