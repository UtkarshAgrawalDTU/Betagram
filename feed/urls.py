from django.urls import path, include
from .views import FeedView

app_name = 'feed'

urlpatterns = [
    path('', FeedView, name = 'home'),
    path('<int:pk>/', include('posts.urls')),
]
