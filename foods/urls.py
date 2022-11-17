from . import views
from django.urls import path

app_name = "foods"

urlpatterns = [
    path("<int:team_pk>/", views.home, name="home"),
    path('<int:team_pk>/store/<int:store_pk>/', views.store_detail, name='store_detail'),
    path('<int:team_pk>/store/all', views.store_all, name='store_all'),
    path('<int:team_pk>/store/<int:store_pk>/follow/', views.store_follow, name='store_follow'),
    path('<int:team_pk>/store/<int:store_pk>/create/', views.store_review_create, name='store_review_create'),
    path('<int:team_pk>/store/<int:store_pk>/<int:review_pk>/delete/', views.store_review_delete, name='store_review_delete'),
    path('<int:team_pk>/<int:tag_pk>/tag/', views.tag, name='tag'),
    path('<int:team_pk>/restaurant_create/', views.restaurant_create, name='restaurant_create'),
    path('<int:team_pk>/restaurant/<int:restaurant_pk>/', views.restaurant_detail, name='restaurant_detail'),
    path('<int:team_pk>/restaurant/<int:restaurant_pk>/follow/', views.restaurant_follow, name='restaurant_follow'),
    path('<int:team_pk>/restaurant/<int:restaurant_pk>/create/', views.restaurant_review_create, name='restaurant_review_create'),
    path('<int:team_pk>/restaurant/<int:restaurant_pk>/<int:review_pk>/delete/', views.restaurant_review_delete, name='restaurant_review_delete'),
    path("<int:team_pk>/search/", views.search, name="search"),
]