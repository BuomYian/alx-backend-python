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
    Handles cascading deletion of:
    - All messages sent by the user (Message model has on_delete=CASCADE)
    - All messages received by the user (Message model has on_delete=CASCADE)
    - All notifications for the user (Notification model has on_delete=CASCADE)
    - All message histories related to user's messages (MessageHistory model has on_delete=CASCADE)

    This demonstrates how post_delete signals can handle complex cleanup operations
    while respecting foreign key relationships. The CASCADE constraints are already
    defined in the models, but this signal provides logging and additional cleanup if needed.
    """
    username = instance.username
    user_id = instance.id

    # Note: Due to CASCADE on_delete constraints in the models, related data is
    # automatically deleted by Django's ORM. However, we log this event for audit purposes.

    EventLog.objects.create(
        event_type='user_deleted',
        description=f"User '{username}' was deleted. All associated messages, notifications, and message histories have been cleaned up.",
        metadata={
            'username': username,
            'user_id': user_id,
            'cleanup_type': 'cascade_delete',
            'deleted_messages': Message.objects.filter(
                sender_id=user_id
            ).count() + Message.objects.filter(
                receiver_id=user_id
            ).count(),
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
