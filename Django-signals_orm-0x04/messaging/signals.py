"""
Signal handlers for the messaging app.
Demonstrates event-driven architecture and best practices.
"""
from django.db.models.signals import post_save, post_delete, pre_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from django.db import transaction
from .models import EventLog, Message, Notification, MessageHistory


@receiver(post_save, sender=User)
def log_user_created_or_updated(sender, instance, created, **kwargs):
    """
    Signal handler that logs when a user is created or updated.
    Demonstrates decoupled side-effect handling.
    """
    event_type = 'user_created' if created else 'user_updated'

    EventLog.objects.create(
        event_type=event_type,
        related_user=instance,
        description=f"User '{instance.username}' was {'created' if created else 'updated'}",
        metadata={
            'username': instance.username,
            'email': instance.email,
        }
    )


@receiver(post_delete, sender=User)
def cleanup_user_data(sender, instance, **kwargs):
    """
    Signal handler that automatically cleans up all user-related data when a user is deleted.
    Demonstrates custom signal logic for cascading deletion:
    - Delete all messages sent and received by the user
    - Delete all notifications for the user
    - Delete all message histories associated with the user's messages

    This shows how to explicitly handle cleanup operations in signals,
    ensuring data integrity and providing detailed logging of what was deleted.
    """
    username = instance.username
    user_id = instance.id

    # Delete message histories for messages sent by this user
    message_history_count = MessageHistory.objects.filter(
        message__sender_id=user_id
    ).delete()[0]

    # Delete all messages where user is the sender or receiver
    messages_sent_count = Message.objects.filter(sender_id=user_id).delete()[0]
    messages_received_count = Message.objects.filter(
        receiver_id=user_id).delete()[0]

    # Delete all notifications for the user
    notifications_count = Notification.objects.filter(
        user_id=user_id).delete()[0]

    total_items_deleted = (
        message_history_count +
        messages_sent_count +
        messages_received_count +
        notifications_count
    )

    # Log the cleanup event for audit purposes
    EventLog.objects.create(
        event_type='user_deleted',
        description=f"User '{username}' account deleted. Cleaned up {total_items_deleted} related records.",
        metadata={
            'username': username,
            'user_id': user_id,
            'cleanup_type': 'signal_cascading_delete',
            'deleted_message_histories': message_history_count,
            'deleted_messages_sent': messages_sent_count,
            'deleted_messages_received': messages_received_count,
            'deleted_notifications': notifications_count,
            'total_deleted': total_items_deleted,
        }
    )


@receiver(pre_save, sender=Message)
def log_message_edit(sender, instance, **kwargs):
    """
    Signal handler that logs message edits using pre_save.
    Captures the old content before the message is updated in the database.
    Demonstrates the importance of using pre_save for audit trails.
    """
    try:
        # Try to get the existing message from the database
        old_instance = Message.objects.get(pk=instance.pk)

        # Check if content or subject has changed
        if old_instance.content != instance.content or old_instance.subject != instance.subject:
            # Only create history if content actually changed
            if old_instance.content != instance.content:
                MessageHistory.objects.create(
                    message=instance,
                    old_content=old_instance.content,
                    old_subject=old_instance.subject,
                    edited_by=instance.sender,
                )

            # Mark message as edited
            instance.edited = True

            # Log the edit event
            EventLog.objects.create(
                event_type='user_updated',
                related_user=instance.sender,
                description=f"Message '{instance.subject}' was edited by {instance.sender.username}",
                metadata={
                    'message_id': instance.id,
                    'old_subject': old_instance.subject,
                    'new_subject': instance.subject,
                }
            )
    except Message.DoesNotExist:
        # This is a new message, so no edit history to log
        pass


@receiver(post_save, sender=Message)
def create_notification_on_message(sender, instance, created, **kwargs):
    """
    Signal handler that automatically creates a notification when a new message is sent.
    Demonstrates event-driven architecture: Message creation → Automatic notification.
    This keeps notification logic decoupled from message creation views.
    """
    if created:
        Notification.objects.create(
            user=instance.receiver,
            notification_type='message_received',
            message=instance,
            title=f"New message from {instance.sender.username}",
            description=f"{instance.sender.username} sent you a message: {instance.subject}",
        )

        # Log the notification event
        EventLog.objects.create(
            event_type='notification_sent',
            related_user=instance.receiver,
            description=f"Notification created for message '{instance.subject}'",
            metadata={
                'message_id': instance.id,
                'sender_id': instance.sender.id,
                'subject': instance.subject,
                'receiver_id': instance.receiver.id,
            }
        )
