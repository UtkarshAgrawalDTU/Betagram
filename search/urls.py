from django.urls import path, include
from .views import SearchResultView
app_name = 'search'

urlpatterns = [
    path('', SearchResultView.as_view(), name = 'search_result'),
]
