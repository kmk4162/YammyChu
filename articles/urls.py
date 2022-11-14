from . import views
from django.urls import path

app_name = "articles"

urlpatterns = [
    path("", views.index, name="index"),
    path("create/", views.create, name="create"),
    path("community/", views.community, name="community"),
    path("community/baseball/", views.baseball, name="baseball"),
    path("community/smalltalk/", views.smalltalk, name="smalltalk"),
    path("community/question/", views.question, name="question"),
    path("community/food/", views.food, name="food"),
    path("community/view/", views.view, name="view"),
    path("community/etc/", views.etc, name="etc"),
    path("community/<int:article_pk>/", views.detail, name="detail"),
    path("<int:article_pk>/update/", views.update, name="update"),
    path("<int:article_pk>/delete/", views.delete, name="delete"),
    path("<int:article_pk>/like/", views.like, name="like"),
    path(
        "<int:article_pk>/comments/create/",
        views.comments_create,
        name="comments_create",
    ),
    path('<int:article_pk>/comments/<int:comment_pk>/update/', views.comments_update, name='comments_update'),
    path('<int:article_pk>/comments/<int:comment_pk>/delete/', views.comments_delete, name='comments_delete'),
]
