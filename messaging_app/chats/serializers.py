from rest_framework import serializers
from chats.models import User, Conversation, Message


class UserSerializer(serializers.ModelSerializer):
    """Serializer for User model."""
    class Meta:
        model = User
        fields = ['id', 'email', 'first_name', 'last_name',
                  'role', 'phone_number', 'created_at']
        read_only_fields = ['id', 'created_at']


class MessageSerializer(serializers.ModelSerializer):
    """Serializer for Message model."""
    sender = UserSerializer(read_only=True)
    sender_id = serializers.UUIDField(write_only=True)

    class Meta:
        model = Message
        fields = ['id', 'conversation', 'sender',
                  'sender_id', 'message_body', 'sent_at']
        read_only_fields = ['id', 'sent_at']


class ConversationDetailSerializer(serializers.ModelSerializer):
    """Detailed serializer for Conversation model with nested messages."""
    participants = UserSerializer(many=True, read_only=True)
    messages = MessageSerializer(many=True, read_only=True)

    class Meta:
        model = Conversation
        fields = ['id', 'participants', 'messages', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']


class ConversationSerializer(serializers.ModelSerializer):
    """Serializer for Conversation model."""
    participants = UserSerializer(many=True, read_only=True)
    participant_ids = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(),
        many=True,
        write_only=True,
        source='participants'
    )

    class Meta:
        model = Conversation
        fields = ['id', 'participants',
                  'participant_ids', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']
