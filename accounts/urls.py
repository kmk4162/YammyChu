from . import views
from django.urls import path

app_name = 'accounts'

urlpatterns = [
    path("signup/", views.signup, name="signup"),
    path("login/", views.login, name="login"),
    path("logout/", views.logout, name="logout"),
    path('<int:pk>/', views.profile, name='profile'),
    path('<int:pk>/follow/', views.follow, name='follow'),
]
