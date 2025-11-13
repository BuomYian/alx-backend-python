from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Chat, Message


class UserSerializer(serializers.ModelSerializer):
    """Serializer for User model."""
    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'email']
        read_only_fields = ['id']


class MessageSerializer(serializers.ModelSerializer):
    """Serializers for Message model."""
    sender = UserSerializer(read_only=True)
    sender_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = Message
        fields = [
            'id', 'chat', 'sender', 'sender_id', 'content', 'is_read', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


class ChatDetailSerializer(serializers.ModelSerializer):
    """Detailed serializer for Chat Model with nested messages."""
    partiicipants = UserSerializer(many=True, read_only=True)
    messages = MessageSerializer(many=True, read_only=True)

    class Meta:
        model = Chat
        fields = ['id', 'name', 'partiicipants',
                  'messages', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']


class ChatSerializer(serializers.ModelSerializer):
    """Serializer for Chat model."""
    participants = UserSerializer(many=True, read_only=True)
    participant_ids = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(),
        many=True,
        write_only=True,
        source='participants'
    )

    class Meta:
        model = Chat
        fields = ['id', 'name', 'participants',
                  'participant_ids', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']
