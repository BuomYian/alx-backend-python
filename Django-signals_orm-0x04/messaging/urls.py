"""
URL configuration for the messaging app.
"""
from django.urls import path
from . import views

app_name = 'messaging'

urlpatterns = [
    path('events/', views.event_log_list, name='event_log_list'),
    path('messages/', views.message_list, name='message_list'),
    path('delete-account/', views.delete_user, name='delete_user'),
]
