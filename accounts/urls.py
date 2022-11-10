from . import views
from django.urls import path

app_name = 'accounts'

urlpatterns = [
    path('<int:pk>/', views.profile, name='profile'),
]
