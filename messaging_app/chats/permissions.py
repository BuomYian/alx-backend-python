"""
Custom permission classes for the messaging API.
Ensure users can only access their own conversations and messages.
"""
from rest_framework.permissions import BasePermission, IsAuthenticated


class IsOwnerOrReadOnly(BasePermission):
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


class IsConversationParticipant(BasePermission):
    """
    Custom permission to only allow participants of a conversation to access it.
    """

    def has_object_permission(self, request, view, obj):
        # Check if the user is a participant in the conversation
        return request.user in obj.participants.all()


class IsMessageSenderOrReadOnly(BasePermission):
    """
    Custom permission to only allow the sender of a message to edit it.
    """

    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to authenticated users
        if request.method in ['GET', 'HEAD', 'OPTIONS']:
            return request.user in obj.conversation.participants.all()
        # Write permissions are only allowed to the sender of the message
        return obj.sender == request.user


class IsAuthenticatedUser(IsAuthenticated):
    """
    Ensure the user is authenticated.
    This class is a simple extension of DRF's IsAuthenticated for clarity.
    """
    pass
