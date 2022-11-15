from . import views
from django.urls import path

app_name = "articles"

urlpatterns = [
    path("", views.index, name="index"),
    path("community/create/", views.create, name="create"),
    path("community/", views.community, name="community"),
    path("community/category/<int:num>", views.category, name="category"),
    path("community/<int:article_pk>/", views.detail, name="detail"),
    path("community/<int:article_pk>/update/", views.update, name="update"),
    path("community/<int:article_pk>/delete/", views.delete, name="delete"),
    path("<int:article_pk>/like/", views.like, name="like"),
    path(
        "<int:article_pk>/comments/create/",
        views.comments_create,
        name="comments_create",
    ),
    path('<int:article_pk>/comments/<int:comment_pk>/update/', views.comments_update, name='comments_update'),
    path('<int:article_pk>/comments/<int:comment_pk>/delete/', views.comments_delete, name='comments_delete'),
]
