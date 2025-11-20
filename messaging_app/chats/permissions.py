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

    def has_object_permission(self, request, view, obj):
        # Check if the user is a participant in the conversation
        if hasattr(obj, 'conversation'):
            return request.user in obj.conversation.participants.all()
        elif hasattr(obj, 'participants'):
            return request.user in obj.participants.all()
        return False


class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow owners of an object to edit it.
    Assumes the model instance has an `owner` attribute.
    """

    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to authenticated users
        if request.method in ['GET', 'HEAD', 'OPTIONS']:
            return True
        # Write permissions are only allowed to the owner of the object
        return obj.sender == request.user or obj.user == request.user


class IsConversationParticipant(permissions.BasePermission):
    """
    Custom permission to only allow participants of a conversation to access it.
    """

    def has_object_permission(self, request, view, obj):
        # Check if the user is a participant in the conversation
        return request.user in obj.participants.all()


class IsMessageSenderOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow the sender of a message to edit it.
    """

    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to authenticated users
        if request.method in ['GET', 'HEAD', 'OPTIONS']:
            return request.user in obj.conversation.participants.all()
        # Write permissions are only allowed to the sender of the message
        return obj.sender == request.user


class IsAuthenticatedUser(permissions.IsAuthenticated):
    """
    Ensure the user is authenticated.
    This class is a simple extension of DRF's IsAuthenticated for clarity.
    """
    pass
