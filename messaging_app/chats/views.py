from rest_framework import viewsets, status, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from .models import Conversation, Message, User
from .serializers import ConversationSerializer, ConversationDetailSerializer, MessageSerializer, UserSerializer
from .permissions import IsConversationParticipant, IsMessageSenderOrReadOnly, IsAuthenticatedUser, IsParticipantOfConversation
from rest_framework.pagination import PageNumberPagination
from django_filters.rest_framework import DjangoFilterBackend
from .pagination import MessagePagination
from .filters import MessageFilter


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet for listing users."""
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticatedUser]
    filter_backends = [filters.SearchFilter]
    search_fields = ['username', 'email']


class ConversationViewSet(viewsets.ModelViewSet):
    """ViewSet for managing Conversation objects."""
    serializer_class = ConversationSerializer
    permission_classes = [IsAuthenticatedUser, IsParticipantOfConversation]
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ['created_at', 'updated_at']
    ordering = ['-updated_at']

    def get_queryset(self):
        """Return conversations for the current user."""
        return Conversation.objects.filter(participants=self.request.user)

    def get_serializer_class(self):
        """Use detailed serializer for retrieve action."""
        if self.action == 'retrieve':
            return ConversationDetailSerializer
        return ConversationSerializer

    def create(self, request, *args, **kwargs):
        """Create a new conversation with participants."""
        participant_ids = request.data.get('participant_ids', [])
        if not participant_ids:
            return Response(
                {'error': 'At least one participant is required'},
                status=status.HTTP_400_BAD_REQUEST
            )

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        conversation = serializer.save()
        # Always add the current user as a participant
        conversation.participants.add(request.user)
        return Response(ConversationSerializer(conversation).data, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticatedUser, IsParticipantOfConversation])
    def send_message(self, request, pk=None):
        """Send a message to a conversation."""
        conversation = self.get_object()

        # Verify user is a participant in the conversation
        if request.user not in conversation.participants.all():
            return Response(
                {'error': 'You are not a participant in this conversation'},
                status=status.HTTP_403_FORBIDDEN
            )

        if not request.data.get('message_body', '').strip():
            return Response(
                {'error': 'Message body cannot be empty'},
                status=status.HTTP_400_BAD_REQUEST
            )

        serializer = MessageSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(conversation=conversation, sender=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['get'], permission_classes=[IsAuthenticatedUser, IsParticipantOfConversation])
    def messages(self, request, pk=None):
        """Get all messages in a conversation."""
        conversation = self.get_object()
        messages = conversation.messages.all().order_by('sent_at')
        serializer = MessageSerializer(messages, many=True)
        return Response(serializer.data)


class MessageViewSet(viewsets.ModelViewSet):
    """ViewSet for managing Message objects."""
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticatedUser,
                          IsMessageSenderOrReadOnly, IsParticipantOfConversation]
    filter_backends = [DjangoFilterBackend,
                       filters.SearchFilter, filters.OrderingFilter]
    filterset_class = MessageFilter
    pagination_class = MessagePagination
    search_fields = ['message_body']
    ordering_fields = ['sent_at']
    ordering = ['-sent_at']

    def get_queryset(self):
        """Return messages from conversations the user participates in."""
        return Message.objects.filter(conversation__participants=self.request.user)

    def create(self, request, *args, **kwargs):
        """Create a new message (should use conversation.send_message instead)."""
        return Response(
            {'error': 'Use the conversation\'s send_message endpoint to create messages'},
            status=status.HTTP_405_METHOD_NOT_ALLOWED
        )

    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticatedUser])
    def by_conversation(self, request):
        """Get messages filtered by conversation_id."""
        conversation_id = request.query_params.get('conversation_id')
        if not conversation_id:
            return Response(
                {'error': 'conversation_id query parameter is required'},
                status=status.HTTP_400_BAD_REQUEST
            )

        messages = self.get_queryset().filter(
            conversation__conversation_id=conversation_id)
        serializer = self.get_serializer(messages, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['patch'], permission_classes=[IsAuthenticatedUser])
    def mark_as_read(self, request, pk=None):
        """Mark a message as read."""
        message = self.get_object()
        message.is_read = True
        message.save()
        serializer = self.get_serializer(message)
        return Response(serializer.data)
