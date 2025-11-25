"""
Views for the messaging app.
Demonstrates efficient ORM queries and caching strategies.
"""
from django.shortcuts import render, redirect
from django.core.cache import cache
from django.views.decorators.cache import cache_page
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.contrib.auth import logout
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


@login_required
def delete_user(request):
    """
    Delete user account and all associated data.
    Uses signals to automatically clean up related data (messages, notifications, history).
    Demonstrates post_delete signal for cascading cleanup operations.

    This view should only be accessible via POST to prevent accidental deletions.
    """
    if request.method == 'POST':
        user = request.user
        username = user.username

        EventLog.objects.create(
            event_type='user_deleted',
            related_user=user,
            description=f"User '{username}' initiated account deletion.",
            metadata={
                'username': username,
                'email': user.email,
                'user_id': user.id,
            }
        )

        user.delete()
        logout(request)

        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return JsonResponse({'status': 'success', 'message': 'Account deleted successfully.'})

        return redirect('home')

    return render(request, 'messaging/delete_user_confirm.html')
