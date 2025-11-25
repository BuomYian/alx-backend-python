"""
App configuration for the messaging module.
Handles signal registration on app startup.
"""
from django.apps import AppConfig


class MessagingConfig(AppConfig):
    """Configure the messaging app and register signals."""
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'messaging'
    verbose_name = 'Event Messaging System'

    def ready(self):
        """Import signal handlers when Django is ready."""
        import messaging.signals  # noqa
