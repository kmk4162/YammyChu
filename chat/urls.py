from . import views
from django.urls import path

app_name = "chat"

urlpatterns = [
    path('<str:room_name>/', views.room, name='room'),
]