from django_filters import rest_framework as filters
from django.utils import timezone
from datetime import timedelta
from .models import Message, Conversation


class MessageFilter(filters.FilterSet):
    """
    Filter class for Message model to enable filtering by:
    - Conversation ID
    - Sender (User)
    - Message sent date range
    - Specific date
    """
    conversation = filters.UUIDFilter(
        field_name='conversation__conversation_id',
        label='Filter by Conversation ID'
    )

    sender = filters.UUIDFilter(
        field_name='sender__user_id',
        label='Filter by Sender User ID'
    )

    sent_after = filters.DateTimeFilter(
        field_name='sent_at',
        lookup_expr='gte',
        label='Messages sent after this date and time'
    )

    sent_before = filters.DateTimeFilter(
        field_name='sent_at',
        lookup_expr='lte',
        label='Messages sent before this date and time'
    )

    search = filters.CharFilter(
        field_name='message_body',
        lookup_expr='icontains',
        label='Search message content'
    )

    class Meta:
        model = Message
        fields = ['conversation', 'sender', 'sent_after',
                  'sent_before', 'search', 'is_read']
