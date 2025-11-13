from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import User


class Chat(models.Model):
    """Model for chat conversations between users."""
    name = models.CharField(max_length=255, blank=True, null=True)
    participants = models.ManyToManyField(User, related_name='chats')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-updated_at']

    def __str__(self):
        return self.name or f"Chat {self.id}"


class Message(models.Model):
    """Model for individual messages within a chat."""
    chat = models.ForeignKey(
        Chat, on_delete=models.CASCADE, related_name='messages')
    sender = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='messages')
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_read = models.BooleanField(default=False)

    class Meta:
        ordering = ['created_at']

    def __str__(self):
        return f"Message from {self.sender.username} in {self.chat}"
