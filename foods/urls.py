from . import views
from django.urls import path

app_name = "foods"

urlpatterns = [
    path("home/", views.home, name="home"),
]
