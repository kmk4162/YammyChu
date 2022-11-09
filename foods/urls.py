from . import views
from django.urls import path

app_name = 'foods'

urlpatterns = [
    path('', views.index, name='index'),
]
