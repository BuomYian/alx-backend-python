"""
Signal handlers for the messaging app.
Demonstrates event-driven architecture and best practices.
"""
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import EventLog, Message, Notification


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
def log_user_deleted(sender, instance, **kwargs):
    """
    Signal handler that logs when a user is deleted.
    Note: We keep the log even after deletion for audit purposes.
    """
    EventLog.objects.create(
        event_type='user_deleted',
        description=f"User '{instance.username}' was deleted",
        metadata={
            'username': instance.username,
            'email': instance.email,
        }
    )


@receiver(post_save, sender=Message)
def create_notification_on_message(sender, instance, created, **kwargs):
    """
    Signal handler that automatically creates a notification when a new message is sent.
    Demonstrates event-driven architecture: Message creation → Automatic notification.
    This keeps notification logic decoupled from message creation views.
    """
    if created:
        Notification.objects.create(
            user=instance.recipient,
            notification_type='message_received',
            message=instance,
            title=f"New message from {instance.sender.username}",
            description=f"{instance.sender.username} sent you a message: {instance.subject}",
        )

        # Log the notification event
        EventLog.objects.create(
            event_type='notification_sent',
            related_user=instance.recipient,
            description=f"Notification created for message '{instance.subject}'",
            metadata={
                'message_id': instance.id,
                'sender_id': instance.sender.id,
                'subject': instance.subject,
                'recipient_id': instance.recipient.id,
            }
        )
