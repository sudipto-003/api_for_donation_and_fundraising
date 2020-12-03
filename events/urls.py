from django.urls import path, include
from .views import *

urlpatterns = [
    path('', EventAPIView.as_view()),
    path('detail/<int:pk>/', EventDetailAPIView.as_view()),
    path('nearevents/', NearEventsAPIView.as_view()),
]