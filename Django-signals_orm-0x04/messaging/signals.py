"""
Signal handlers for the messaging app.
Demonstrates event-driven architecture and best practices.
"""
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.contrib.auth.models import User
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
def log_message_sent(sender, instance, created, **kwargs):
    """
    Signal handler that logs message edits using pre_save.
    Captures the old content before the message is updated in the database.
    Demonstrates the importance of using pre_save for audit trails.
    """
    try:
        old_instance = Message.objects.get(pk=instance.pk)

        if old_instance.content != instance.content or old_instance.subject != instance.subject:
            if old_instance.content != instance.content:
                MessageHistory.objects.create(
                    message=instance,
                    old_content=old_instance.content,
                    old_subject=old_instance.subject,
                    edited_by=instance.sender,
                )

                instance.edited = True

                EventLog.objects.create(
                    event_type='user_updated',
                    related_user=instance.sender,
                    description=f"Message '{instance.subject}' was edited by '{instance.sender.username}'",
                    metadata={
                        'message_id': instance.id,
                        'old_subject': old_instance.subject,
                        'new_subject': instance.subject,
                    }
                )

    except Message.DoesNotExist:
        # Message is new, no old instance to compare
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
