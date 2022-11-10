from django.shortcuts import render, redirect
from .models import Article, Comment
from .forms import ArticleForm, CommentForm
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
import json

def index(request):
    
    return render(request, 'articles/index.html')

@login_required
def create(request):
    if request.method == 'POST':
        article_form = ArticleForm(request.POST)
        if article_form.is_valid():
            article = article_form.save(commit=False)
            article.user = request.user
            article.save()
            return redirect('articles:community')
    else:
        article_form = ArticleForm()
    context = {
        'article_form': article_form,
    }
    return render(request, 'articles/create.html', context)

@login_required
def update(request, article_pk):
    article = Article.objects.get(pk=article_pk)
    if request.method == 'POST':
        article_form = ArticleForm(request.POST, instance=article)
        if article_form.is_valid():
            article_form.save()
            return redirect('articles:community')
    else:
        article_form = ArticleForm()
    context = {
        'article_form': article_form,
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
def like(request):

    return redirect('articles:index')

@login_required
def community(request):

    return render(request, 'articles/community.html')

def detail(request, article_pk):
    article = Article.objects.get(pk=article_pk)
    comments = article.comment_set.all().order_by('-pk')
    comment_form = CommentForm()
    context = {
        'article' : article,
        'comment_form' : comment_form,
        'comments' : comments,
    }
    return render(request, 'articles/detail.html', context)
