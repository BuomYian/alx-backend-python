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
from django.db.models import Prefetch, Q
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
def conversation_thread(request, message_id):
    """
    Display a threaded conversation with optimized queries.
    Uses select_related and prefetch_related to minimize database hits.

    New view for displaying threaded conversations efficiently
    """
    try:
        # Get the root message with optimized query
        root_message = Message.objects.select_related(
            'sender',
            'receiver',
            'parent_message__sender',
        ).get(id=message_id)
    except Message.DoesNotExist:
        return JsonResponse({'error': 'Message not found'}, status=404)

    # Check if user has permission to view this conversation
    if request.user != root_message.sender and request.user != root_message.receiver:
        return JsonResponse({'error': 'Permission denied'}, status=403)

    # Prefetch all replies in a single query to avoid N+1 problem
    replies_prefetch = Prefetch(
        'replies',
        queryset=Message.objects.select_related(
            'sender', 'receiver').order_by('timestamp')
    )

    root_message = Message.objects.prefetch_related(
        replies_prefetch).get(id=message_id)

    # Build threaded conversation structure
    threaded_messages = build_thread_structure(root_message)

    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse(threaded_messages, safe=False)

    return render(request, 'messaging/conversation_thread.html', {
        'root_message': root_message,
        'threaded_messages': threaded_messages
    })


def build_thread_structure(message, depth=0):
    """
    Recursively build a threaded message structure for display.

    New utility function for displaying messages in threaded format
    """
    thread = {
        'id': message.id,
        'sender': message.sender.username,
        'receiver': message.receiver.username,
        'subject': message.subject,
        'content': message.content,
        'timestamp': message.timestamp.isoformat(),
        'is_read': message.is_read,
        'edited': message.edited,
        'depth': depth,
        'replies': [
            build_thread_structure(reply, depth + 1)
            for reply in message.replies.all()
        ]
    }
    return thread


@login_required
def send_reply(request, parent_message_id):
    """
    Send a reply to an existing message, creating a threaded conversation.

    New view for posting replies to messages
    """
    if request.method == 'POST':
        try:
            parent_message = Message.objects.select_related('sender', 'receiver').get(
                id=parent_message_id
            )
        except Message.DoesNotExist:
            return JsonResponse({'error': 'Parent message not found'}, status=404)

        # Determine who the reply should go to
        if request.user == parent_message.sender:
            receiver = parent_message.receiver
        elif request.user == parent_message.receiver:
            receiver = parent_message.sender
        else:
            return JsonResponse({'error': 'Permission denied'}, status=403)

        # Get the root message of the thread
        root_message = parent_message
        while root_message.parent_message:
            root_message = root_message.parent_message

        # Create the reply
        reply = Message.objects.create(
            sender=request.user,
            receiver=receiver,
            parent_message=parent_message,
            subject=f"Re: {root_message.subject}",
            content=request.POST.get('content', ''),
        )

        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({
                'success': True,
                'message_id': reply.id,
                'message': 'Reply sent successfully'
            })

        return redirect('conversation_thread', message_id=parent_message_id)

    return JsonResponse({'error': 'Method not allowed'}, status=405)


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

        # Log the deletion event before deletion
        EventLog.objects.create(
            event_type='user_deleted',
            related_user=user,
            description=f"User '{username}' initiated account deletion",
            metadata={
                'username': username,
                'email': user.email,
                'user_id': user.id,
            }
        )

        # Delete the user - post_delete signal will handle cleanup
        user.delete()

        # Logout the user (redundant after deletion, but safe)
        logout(request)

        # Return JSON response or redirect to home
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({'success': True, 'message': 'Account deleted successfully'})

        return redirect('home')

    # For GET requests, return a confirmation page
    return render(request, 'messaging/delete_user_confirm.html')


@login_required
def unread_messages(request):
    """
    Display unread messages for the authenticated user.
    Uses the custom UnreadMessagesManager with .only() optimization.

    New view for displaying unread messages with optimized queries
    """
    # Use custom manager to get unread messages with optimized fields
    unread_msgs = Message.unread.unread_for_user(request.user)

    # Get the count of unread messages
    unread_count = Message.unread.unread_count_for_user(request.user)

    # Cache the unread count for quick access
    cache_key = f'unread_count_{request.user.id}'
    cache.set(cache_key, unread_count, 60)  # Cache for 1 minute

    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        # Return JSON for AJAX requests
        messages_data = [
            {
                'id': msg.id,
                'sender': msg.sender.username,
                'subject': msg.subject,
                'content': msg.content[:100],  # First 100 chars
                'timestamp': msg.timestamp.isoformat(),
            }
            for msg in unread_msgs
        ]
        return JsonResponse({
            'unread_count': unread_count,
            'messages': messages_data
        })

    return render(request, 'messaging/unread_messages.html', {
        'unread_messages': unread_msgs,
        'unread_count': unread_count,
    })


@login_required
def mark_as_read(request, message_id):
    """
    Mark a message as read by the current user.
    Only the receiver can mark a message as read.

    New view for marking messages as read
    """
    if request.method == 'POST':
        try:
            message = Message.objects.get(id=message_id, receiver=request.user)
            message.is_read = True
            message.save(update_fields=['is_read'])

            # Invalidate the unread count cache
            cache_key = f'unread_count_{request.user.id}'
            cache.delete(cache_key)

            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({'success': True, 'message': 'Message marked as read'})

            return redirect('unread_messages')
        except Message.DoesNotExist:
            return JsonResponse({'error': 'Message not found'}, status=404)

    return JsonResponse({'error': 'Method not allowed'}, status=405)


@login_required
def inbox_dashboard(request):
    """
    Display inbox dashboard with unread count and recent messages.
    Demonstrates efficient use of custom managers and caching.

    New view for inbox dashboard
    """
    # Get cached unread count or calculate it
    cache_key = f'unread_count_{request.user.id}'
    unread_count = cache.get(cache_key)

    if unread_count is None:
        unread_count = Message.unread.unread_count_for_user(request.user)
        cache.set(cache_key, unread_count, 60)

    # Get recent unread messages (first 5)
    recent_unread = Message.unread.unread_for_user(request.user)[:5]

    # Get all recent messages (read and unread) for context
    all_recent = Message.objects.filter(
        receiver=request.user
    ).select_related('sender').only(
        'id',
        'sender__username',
        'subject',
        'timestamp',
        'is_read',
    ).order_by('-timestamp')[:10]

    return render(request, 'messaging/inbox_dashboard.html', {
        'unread_count': unread_count,
        'recent_unread': recent_unread,
        'all_recent': all_recent,
    })
