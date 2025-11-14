from rest_framework import serializers
from chats.models import User, Conversation, Message


class UserSerializer(serializers.ModelSerializer):
    """Serializer for User model with custom UUID primary key."""
    class Meta:
        model = User
        fields = ['user_id', 'username', 'email', 'first_name',
                  'last_name', 'role', 'phone_number', 'created_at', 'updated_at']
        read_only_fields = ['user_id', 'created_at', 'updated_at']


class MessageSerializer(serializers.ModelSerializer):
    """Serializer for Message model with nested sender information."""
    sender = UserSerializer(read_only=True)
    sender_id = serializers.UUIDField(write_only=True)

    class Meta:
        model = Message
        fields = ['message_id', 'conversation', 'sender', 'sender_id',
                  'message_body', 'sent_at', 'updated_at', 'is_read']
        read_only_fields = ['message_id', 'sent_at', 'updated_at']


class ConversationSerializer(serializers.ModelSerializer):
    """Serializer for Conversation model listing participants."""
    participants = UserSerializer(many=True, read_only=True)
    participant_ids = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(),
        many=True,
        write_only=True,
        source='participants'
    )

    class Meta:
        model = Conversation
        fields = ['conversation_id', 'participants',
                  'participant_ids', 'created_at', 'updated_at']
        read_only_fields = ['conversation_id', 'created_at', 'updated_at']


class ConversationDetailSerializer(serializers.ModelSerializer):
    """Detailed serializer for Conversation with nested messages and participants."""
    participants = UserSerializer(many=True, read_only=True)
    messages = MessageSerializer(many=True, read_only=True)
    participant_ids = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(),
        many=True,
        write_only=True,
        source='participants'
    )

    class Meta:
        model = Conversation
        fields = ['conversation_id', 'participants',
                  'participant_ids', 'messages', 'created_at', 'updated_at']
        read_only_fields = ['conversation_id', 'created_at', 'updated_at']
