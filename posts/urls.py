from django.contrib import admin
from django.urls import path, include
from .views import PostDetailView, PostUpdateView, PostDeleteView
app_name = 'posts'

urlpatterns = [
    path('', PostDetailView.as_view(), name ='post_detail'),
    path('update/', PostUpdateView.as_view(), name = 'post_update'),
    path('delete/', PostDeleteView.as_view(), name= 'post_delete'),
]
