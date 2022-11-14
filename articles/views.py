from django.shortcuts import render, redirect
from .models import Article, Comment, Team
from .forms import ArticleForm, CommentForm
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
import json
from django.core.paginator import Paginator  


def index(request):
    teams = Team.objects.all()
    context = {
        "teams": teams,
    }
    return render(request, "articles/index.html", context)


@login_required
def create(request):
    if request.method == "POST":
        article_form = ArticleForm(request.POST)
        if article_form.is_valid():
            article = article_form.save(commit=False)
            article.user = request.user
            article.save()
            return redirect('articles:community')
    else:
        article_form = ArticleForm()
    context = {
        "article_form": article_form,
    }
    return render(request, 'articles/create.html', context)

@login_required
def update(request, article_pk):
    article = Article.objects.get(pk=article_pk)
    if request.method == "POST":
        article_form = ArticleForm(request.POST, instance=article)
        if article_form.is_valid():
            article_form.save()
            return redirect("articles:community")
    else:
        article_form = ArticleForm()
    context = {
        "article_form": article_form,
    }
    return render(request, 'articles/update.html', context)

@login_required
def delete(request, article_pk):
    article = Article.objects.get(pk=article_pk)
    if request.user == article.user:
        article.delete()
        return redirect('articles:index')

@login_required
def comments_create(request, article_pk):
    article = Article.objects.get(pk=article_pk)
    comment_form = CommentForm(request.POST)
    user = request.user.pk
    if comment_form.is_valid():
        comment = comment_form.save(commit=False)
        comment.article = article
        comment.user = request.user
        comment.save()
    temp = Comment.objects.filter(article_id=article_pk).order_by('-pk')
    comment_data = []
    for t in temp:
        comment_data.append({
            'userId': t.user_id, 
            'userName': t.user.username, 
            'content': t.content,
            'commentPk': t.pk,
        })
    context = {
        'comment_data': comment_data,
        'article_pk': article_pk,
        'user': user,
    }
    return JsonResponse(context)

@login_required
def comments_update(request, article_pk, comment_pk):
    comment = Comment.objects.get(pk=comment_pk)
    comment_username = comment.user.username
    user = request.user.pk
    jsonObject = json.loads(request.body)
    if request.method == 'POST':
        comment.content = jsonObject.get('content')
        comment.save()
    temp = Comment.objects.filter(article_id=article_pk).order_by('-pk')
    comment_data = []
    for t in temp:
        comment_data.append({
            'userId':t.user_id, 
            'userName': t.user.username, 
            'content': t.content,
            'commentPk': t.pk,
        })
    context = {
        'comment_data': comment_data,
        'comment_pk': comment_pk,
        'comment_username': comment_username,
        'article_pk': article_pk,
        'user': user,
    }
    return JsonResponse(context)

@login_required
def comments_delete(request, article_pk, comment_pk):
    comment = Comment.objects.get(pk=comment_pk)
    article_pk = Article.objects.get(pk=article_pk).pk
    user = request.user.pk
    comment.delete()
    temp = Comment.objects.filter(article_id=article_pk).order_by('-pk')
    comment_data = []
    for t in temp:
        comment_data.append({
            'userId':t.user_id, 
            'userName': t.user.username, 
            'content': t.content,
            'commentPk': t.pk,
        })
    context = {
        'comment_data': comment_data,
        'article_pk': article_pk,
        'user': user,
    }
    return JsonResponse(context)

@login_required
def like(request, article_pk):
    article = Article.objects.get(pk=article_pk)
    if article.user_article_like.filter(pk=request.user.pk).exists():
        article.user_article_like.remove(request.user)
        is_liked = False
    else:
        article.user_article_like.add(request.user)
        is_liked = True
    likeCount = article.user_article_like.count()
    article.like_count = likeCount
    context = {
        'isLiked' : is_liked,
        'likeCount' : article.user_article_like.count(),
    }
    return JsonResponse(context)


def community(request):
    articles = Article.objects.all().order_by('-pk')
    # 입력 파라미터
    page = request.GET.get("page", "1")
    # 페이징
    paginator_all = Paginator(articles, 10)
    page_obg_all = paginator_all.get_page(page)
    context = {
        'articles' : articles,
        'articles_all' : page_obg_all,
    }
    return render(request, 'articles/community.html', context)

def baseball(request):
    articles_baseball = Article.objects.filter(category='야구').order_by('-pk')
    page = request.GET.get("page", "1")
    paginator_baseball = Paginator(articles_baseball, 2)
    page_obg_baseball = paginator_baseball.get_page(page)
    context = {
        'articles_baseball' : page_obg_baseball,
    }
    return render(request, 'articles/baseball.html', context)

def smalltalk(request):
    articles_smalltalk = Article.objects.filter(category='잡담').order_by('-pk')
    page = request.GET.get("page", "1")
    paginator_smalltalk = Paginator(articles_smalltalk, 10)
    page_obg_smalltalk = paginator_smalltalk.get_page(page)
    context = {
        'articles_smalltalk' : page_obg_smalltalk,
    }
    return render(request, 'articles/smalltalk.html', context)

def question(request):
    articles_question = Article.objects.filter(category='질문').order_by('-pk')
    page = request.GET.get("page", "1")
    paginator_question = Paginator(articles_question, 10)
    page_obg_question = paginator_question.get_page(page)
    context = {
        'articles_question' : page_obg_question,
    }
    return render(request, 'articles/question.html', context)

def food(request):
    articles_food = Article.objects.filter(category='음식').order_by('-pk')
    page = request.GET.get("page", "1")
    paginator_food = Paginator(articles_food, 10)
    page_obg_food = paginator_food.get_page(page)
    context = {
        'articles_food' : page_obg_food,
    }
    return render(request, 'articles/food.html', context)

def view(request):
    articles_view = Article.objects.filter(category='직관모집').order_by('-pk')
    page = request.GET.get("page", "1")
    paginator_view = Paginator(articles_view, 10)
    page_obg_view = paginator_view.get_page(page)
    context = {
        'articles_view' : page_obg_view,
    }
    return render(request, 'articles/view.html', context)

def etc(request):
    articles_etc = Article.objects.filter(category='기타').order_by('-pk')
    page = request.GET.get("page", "1")
    paginator_etc = Paginator(articles_etc, 10)
    page_obg_etc = paginator_etc.get_page(page)
    context = {
        'articles_etc' : page_obg_etc,
    }
    return render(request, 'articles/etc.html', context)

def detail(request, article_pk):
    article = Article.objects.get(pk=article_pk)
    comments = article.comment_set.all().order_by('-pk')
    comment_form = CommentForm()
    context = {
        'article' : article,
        'comment_form' : comment_form,
        'comments' : comments,
    }
    return render(request, "articles/detail.html", context)
