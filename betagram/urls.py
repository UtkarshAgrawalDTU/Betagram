from django.contrib import admin
from django.urls import path, include
from users.views import UserLogoutView, UserLoginView, UserRegisterView, ProfileView, EditProfileView, RequestView, FollowerListView, FollowingListView
from django.conf.urls.static import static
from . import settings
from posts.views import PostCreateView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', UserLoginView.as_view(), name = 'login'),
    path('logout/', UserLogoutView.as_view(), name = 'logout'),
    path('register/', UserRegisterView, name = 'register'),
    path('', include('feed.urls')),
    path('<int:pk>/', include('posts.urls')),
    path('search/', include('search.urls')),
    path('notifications/', include('notifications.urls')),
    path('profile-<username>/', ProfileView, name = 'profile'),
    path('profile-<username>/followers/', FollowerListView, name = 'follower_list'),
    path('profile-<username>/following/', FollowingListView, name = 'following_list'),
    path('profile-<username>/edit/', EditProfileView, name = 'profile-edit'),
    path('create/', PostCreateView.as_view(), name = 'create'),
    path('requests/', RequestView, name = 'requests'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)