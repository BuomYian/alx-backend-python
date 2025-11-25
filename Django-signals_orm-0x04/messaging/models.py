"""
Models for the messaging app.
Demonstrates efficient database design for event handling.
"""
from django.db import models
from django.contrib.auth.models import User


class EventLog(models.Model):
    """
    Logs all events triggered by signals.
    Useful for debugging and understanding signal behavior.
    """
    EVENT_TYPES = [
        ('user_created', 'User Created'),
        ('user_updated', 'User Updated'),
        ('user_deleted', 'User Deleted'),
        ('email_sent', 'Email Sent'),
        ('notification_sent', 'Notification Sent'),
    ]

    event_type = models.CharField(
        max_length=50,
        choices=EVENT_TYPES,
        db_index=True,
    )
    related_user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='event_logs',
        null=True,
        blank=True,
    )
    description = models.TextField()
    metadata = models.JSONField(default=dict, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-timestamp']
        indexes = [
            models.Index(fields=['event_type', '-timestamp']),
        ]

    def __str__(self):
        return f"{self.get_event_type_display()} - {self.timestamp}"


class Message(models.Model):
    """
    Represents a message in the system.
    Demonstrates ORM relationships and query optimization.
    """
    sender = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='sent_messages',
    )
    receiver = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='received_messages',
    )
    subject = models.CharField(max_length=200)
    content = models.TextField()
    is_read = models.BooleanField(default=False, db_index=True)
    timestamp = models.DateTimeField(auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-timestamp']
        indexes = [
            models.Index(fields=['receiver', 'is_read']),
            models.Index(fields=['sender', '-timestamp']),
        ]

    def __str__(self):
        return f"Message from {self.sender} to {self.receiver}: {self.subject}"


class MessagingHistory(models.Model):
    """
    Stores the history of message edits.
    Each time a message is edited, the old content is saved here.
    Demonstrates use of pre_save signal for audit logging.
    """
    message = models.ForeignKey(
        Message,
        on_delete=models.CASCADE,
        related_name='history',
    )
    old_content = models.TextField()
    old_subject = models.CharField(max_length=200, blank=True)
    edited_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='message_edits',
    )
    edited_at = models.DateTimeField(auto_now_add=True, db_index=True)

    class Meta:
        ordering = ['-edited_at']
        indexes = [
            models.Index(fields=['message', '-edited_at']),
        ]

    def __str__(self):
        return f"Edit history for Message ID {self.message.id} at {self.edited_at}"


class Notification(models.Model):
    """
    Stores notifications for users.
    Automatically created via signals when messages are received.
    Demonstrates signal-driven, decoupled notification system.
    """
    NOTIFICATIONS_TYPES = [
        ('message_received', 'Message Received'),
        ('message_read', 'Message Read'),
        ('user_event', 'User Event'),
    ]

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='notifications',
    )
    notification_type = models.CharField(
        max_length=50,
        choices=NOTIFICATIONS_TYPES,
        db_index=True,
    )
    message = models.ForeignKey(
        Message,
        on_delete=models.CASCADE,
        related_name='notifications',
        null=True,
        blank=True,
    )
    title = models.CharField(max_length=200)
    description = models.TextField()
    is_read = models.BooleanField(default=False, db_index=True)
    timestamp = models.DateTimeField(auto_now_add=True, db_index=True)
    read_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ['-timestamp']
        indexes = [
            models.Index(fields=['user', 'is_read']),
            models.Index(fields=['user', '-timestamp']),
        ]

    def __str__(self):
        return f"Notification for {self.user}: {self.title}"
