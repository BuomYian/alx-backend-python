"""
Custom managers for the messaging app.
Demonstrates advanced ORM query optimization techniques.
"""
from django.db import models


class UnreadMessagesManager(models.Manager):
    """
    Custom manager to filter unread messages for a specific user.
    Demonstrates query optimization using .only() and select_related().
    """

    def unread_for_user(self, user):
        """
        Returns all unread messages received by a user.
        Uses only() to optimize database queries by fetching only necessary fields.

        Args:
            user: The User instance to fetch unread messages for

        Returns:
            QuerySet of unread messages optimized for minimal data retrieval
        """
        return self.filter(
            receiver=user,
            read=False
        ).select_related('sender').only(
            'id',
            'sender__id',
            'sender__username',
            'sender__email',
            'subject',
            'content',
            'timestamp',
            'read',
        ).order_by('-timestamp')

    def unread_count_for_user(self, user):
        """
        Returns the count of unread messages for a user.
        Optimized query that only counts without fetching full objects.
        """
        return self.filter(receiver=user, read=False).count()
