"""
Signal handlers for the messaging app.
Demonstrates event-driven architecture and best practices.
"""
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import EventLog


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
