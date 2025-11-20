"""
Custom permission classes for the messaging API.
Ensure users can only access their own conversations and messages.
"""
from rest_framework import permissions


class IsParticipantOfConversation(permissions.BasePermission):
    """
    Permission class to allow only participants of a conversation to:
    - Send messages
    - View messages
    - Update messages
    - Delete messages

    This is the primary permission for conversation and message access control.
    """

    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        if not request.user or not request.user.is_authenticated:
            return False
        # Check if the user is a participant in the conversation
        if hasattr(obj, 'conversation'):
            is_participant = request.user in obj.conversation.participants.all()
        elif hasattr(obj, 'participants'):
            is_participant = request.user in obj.participants.all()
        else:
            is_participant = False

        # Allow GET, HEAD, OPTIONS for participants
        if request.method in ['GET', 'HEAD', 'OPTIONS']:
            return is_participant

        if request.method in ['PUT', 'PATCH', 'DELETE']:
            # For messages, only the sender can update or delete
            if hasattr(obj, 'sender'):
                return obj.sender == request.user and is_participant
            # For conversations, any participant can update or delete
            return is_participant

        return is_participant


class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow owners of an object to edit it.
    Assumes the model instance has an `owner` attribute.
    """

    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to authenticated users
        if request.method in ['GET', 'HEAD', 'OPTIONS']:
            return request.user.is_authenticated
        if request.method in ['PUT', 'PATCH', 'DELETE']:
            # Write permissions are only allowed to the owner of the object
            return obj.sender == request.user or obj.user == request.user

        return False


class IsConversationParticipant(permissions.BasePermission):
    """
    Custom permission to only allow participants of a conversation to access it.
    """

    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        # Check if the user is a participant in the conversation
        return request.user.is_authenticated and request.user in obj.participants.all()


class IsMessageSenderOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow the sender of a message to edit it.
    """

    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to authenticated users
        if request.method in ['GET', 'HEAD', 'OPTIONS']:
            return request.user.is_authenticated and request.user in obj.conversation.participants.all()
        if request.method in ['PUT', 'PATCH', 'DELETE']:
            # Write permissions are only allowed to the sender of the message
            return obj.sender == request.user
        return False


class IsAuthenticatedUser(permissions.IsAuthenticated):
    """
    Ensure the user is authenticated.
    This class is a simple extension of DRF's IsAuthenticated for clarity.
    """
    pass
