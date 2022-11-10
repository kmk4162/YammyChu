from django.shortcuts import render, redirect

def index(request):
    
    return render(request, 'articles/index.html')

def create(request):
    
    return render(request, 'articles/create.html')

def update(request):

    return render(request, 'articles/update.html')

def delete(request):

    return redirect('articles:index')

def comments_create(request):

    return redirect('articles:index')

def like(request):

    return redirect('articles:index')

def detail(request):

    return render(request, 'articles/detail.html')
