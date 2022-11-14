from . import views
from django.urls import path

app_name = "foods"

urlpatterns = [
    path("home/<int:team_pk>/", views.home, name="home"),
    path('home/<int:team_pk>/<int:store_pk>/', views.detail, name='detail'),
    path('home/<int:team_pk>/<int:store_pk>/create/', views.create, name='create'),
    path('home/<int:team_pk>/<int:store_pk>/<int:review_pk>/delete/', views.delete, name='delete'),
    # path('home/<int:team_pk>/<int:tag_pk>', views.tag, name='tag'),
]