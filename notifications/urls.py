from django.contrib import admin
from django.urls import path, include
from .views import NotifView
app_name = 'notifs'

urlpatterns = [
    path('', NotifView, name = 'notification_page')
]
