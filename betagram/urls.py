from django.contrib import admin
from django.urls import path, include
from users.views import UserLogoutView, UserLoginView, UserRegisterView, ProfileView, EditProfileView, RequestView
from django.conf.urls.static import static
from . import settings
from posts.views import PostCreateView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', UserLoginView.as_view(), name = 'login'),
    path('logout/', UserLogoutView.as_view(), name = 'logout'),
    path('', include('feed.urls')),
    path('<int:pk>/', include('posts.urls')),
    path('register/', UserRegisterView, name = 'register'),
    path('profile-<username>/', ProfileView, name = 'profile'),
    path('profile-<username>/edit/', EditProfileView, name = 'profile-edit'),
    path('create/', PostCreateView.as_view(), name = 'create'),
    path('search/', include('search.urls')),
    path('requests/', RequestView, name = 'requests'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)