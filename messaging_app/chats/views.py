from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from .models import Chat, Message
from .serializers import ChatSerializer, ChatDetailSerializer, MessageSerializer


class ChatViewSet(viewsets.ModelViewSet):
    """ViewSet for managing Chat objects."""
    serializer_class = ChatSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """Return chats for the current user."""
        return Chat.objects.filter(participants=self.request.user)

    def get_serializer_class(self):
        """Return appropriate serializer class based on action."""
        if self.action == 'retrieve':
            return ChatDetailSerializer
        return ChatSerializer

    def create(self, request, *args, **kwargs):
        """Create a new chat."""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        chat = serializer.save()
        chat.participants.add(request.user)
        return Response(ChatSerializer(chat).data, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def send_message(self, request, pk=None):
        """Sned a message in the specified chat."""
        chat = self.get_object()
        serializer = MessageSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(chat=chat, sender=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['get'], permission_classes=[IsAuthenticated])
    def messages(self, request, pk=None):
        """Retrieve messages for the specified chat."""
        chat = self.get_object()
        messages = chat.messages.all()
        serializer = MessageSerializer(messages, many=True)
        return Response(serializer.data)
