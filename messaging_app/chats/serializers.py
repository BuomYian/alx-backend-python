from rest_framework import serializers
from .models import User, Conversation, Message


class UserSerializer(serializers.ModelSerializer):
    """Serializer for User model with custom UUID primary key."""
    username = serializers.CharField(required=True)

    class Meta:
        model = User
        fields = ['user_id', 'username', 'email', 'first_name',
                  'last_name', 'role', 'phone_number', 'created_at', 'updated_at']
        read_only_fields = ['user_id', 'created_at', 'updated_at']

    def validate_username(self, value):
        if len(value) < 3:
            raise serializers.ValidationError(
                "Username must be at least 3 characters long.")
        return value


class MessageSerializer(serializers.ModelSerializer):
    """Serializer for Message model with nested sender information."""
    sender = UserSerializer(read_only=True)
    sender_id = serializers.UUIDField(write_only=True)
    message_preview = serializers.SerializerMethodField()

    class Meta:
        model = Message
        fields = ['message_id', 'conversation', 'sender', 'sender_id',
                  'message_body', 'message_preview', 'sent_at', 'updated_at', 'is_read']
        read_only_fields = ['message_id', 'sent_at',
                            'updated_at', 'message_preview']

    def get_message_preview(self, obj):
        return obj.message_body[:50] + '...' if len(obj.message_body) > 50 else obj.message_body


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
    participant_count = serializers.SerializerMethodField()

    class Meta:
        model = Conversation
        fields = ['conversation_id', 'participants', 'participant_ids',
                  'participant_count', 'messages', 'created_at', 'updated_at']
        read_only_fields = ['conversation_id',
                            'created_at', 'updated_at', 'participant_count']

    def get_participant_count(self, obj):
        return obj.participants.count()
