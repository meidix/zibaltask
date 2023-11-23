from django.urls import path
from .views import *

urlpatterns = [
    path('', NotificationService.as_view()),
]