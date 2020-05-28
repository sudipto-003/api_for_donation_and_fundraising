from django.urls import path, include
from knox.views import LogoutView
from .views import *

urlpatterns = [
    path('login/', UserLoginAPIView.as_view()),
    path('register/', UserRegistrationAPIView.as_view()),
    path('user/', UserAPIView.as_view()),
    path('userinfo/', UserInfoAPIView.as_view()),
    path('userdetail/<int:pk>/', UserDetailAPIView.as_view()),
    path('usercontact/', UserContactAPIView.as_view()),
    path('usersite/', UserSiteAPIView.as_view()),
    path('', include('knox.urls')),
]