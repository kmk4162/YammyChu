from django.shortcuts import render, redirect
from .models import Article
from .forms import ArticleForm
from django.contrib.auth.decorators import login_required


def index(request):
    
    return render(request, 'articles/index.html')

def create(request):
    if request.method == 'POST':
        article_form = ArticleForm(request.POST)
        if article_form.is_valid():
            article_form.save()
            return redirect('articles:community')
    else:
        article_form = ArticleForm()
    context = {
        'article_form': article_form,
    }
    return render(request, 'articles/create.html', context)

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

def delete(request):

    return redirect('articles:index')

def comments_create(request):

    return redirect('articles:index')

def like(request):

    return redirect('articles:index')

def detail(request, article_pk):
    article = Article.objects.get(pk=article_pk)
    context = {
        'article' : article,
    }
    return render(request, 'articles/detail.html', context)
