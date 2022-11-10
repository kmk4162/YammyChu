from . import views
from django.urls import path

app_name = "foods"

urlpatterns = [
    path("home/<int:team_pk>", views.home, name="home"),
    path('<int:store_pk>/detail', views.detail, name='detail'),
    path('<int:store_pk>/create', views.create, name='create'),
]