from . import views
from django.urls import path

app_name = 'articles'

urlpatterns = [
    path('', views.index, name='index'),
    path('create/', views.create, name='create'),
    path('<int:article_pk>/', views.detail, name='detail'),
    path('<int:article_pk>/update/', views.update, name='update'),
    path('<int:article_pk>/delete/', views.delete, name='delete'),
    path('like/', views.like, name='like'),
    path('<int:article_pk>/comments/create/', views.comments_create, name='comments_create'),
    path('community/', views.community, name='community'),
]
