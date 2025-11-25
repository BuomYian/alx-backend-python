"""
URL configuration for the messaging app.
"""
from django.urls import path
from . import views

app_name = 'messaging'

urlpatterns = [
    path('events/', views.event_log_list, name='event_log_list'),
    path('messages/', views.message_list, name='message_list'),
    path('conversation/<int:message_id>/',
         views.conversation_thread, name='conversation_thread'),
    path('conversation/<int:parent_message_id>/reply/',
         views.send_reply, name='send_reply'),
    path('delete-account/', views.delete_user, name='delete_user'),
    path('inbox/', views.inbox_dashboard, name='inbox_dashboard'),
    path('unread/', views.unread_messages, name='unread_messages'),
    path('message/<int:message_id>/mark-as-read/',
         views.mark_as_read, name='mark_as_read'),
]
