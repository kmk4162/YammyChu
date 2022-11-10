from . import views
from django.urls import path

app_name = 'foods'

urlpatterns = [
    path('', views.index, name='index'),
    # path('<int:store_pk>/detail', views.detail, name='detail'),
    path('detail', views.detail, name='detail'),
]
