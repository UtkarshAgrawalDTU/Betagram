from django.contrib import admin
from django.urls import path, include
from .views import PostDetailView
app_name = 'posts'

urlpatterns = [
    path('', PostDetailView.as_view(), name ='post_detail'),
]
