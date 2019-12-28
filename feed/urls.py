from django.contrib import admin
from django.urls import path, include
from .views import FeedView

app_name = 'feed'

urlpatterns = [
    path('', FeedView, name = 'home'),
]
