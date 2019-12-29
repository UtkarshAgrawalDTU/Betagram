from django.contrib import admin
from django.urls import path, include
from users.views import UserLogoutView, UserLoginView, UserRegisterView, ProfileView, EditProfileView
from django.conf.urls.static import static
from . import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', UserLoginView.as_view(), name = 'login'),
    path('logout/', UserLogoutView.as_view(), name = 'logout'),
    path('', include('feed.urls')),
    path('<int:pk>/', include('posts.urls')),
    path('register/', UserRegisterView, name = 'register'),
    path('profile-<str:username>/', ProfileView, name = 'profile'),
    path('profile-<str:username>/edit/', EditProfileView, name = 'profile-edit'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)