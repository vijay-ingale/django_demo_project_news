from django.urls import path
from .views import UserLogin, SearchAPI, SearchResult

urlpatterns = [
    path('login/', UserLogin.as_view(), name='user_login'),
    path('search/', SearchAPI.as_view(), name='Search'),
    path('result/', SearchResult.as_view(), name='Searching_result')
]
