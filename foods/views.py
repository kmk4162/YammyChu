from django.shortcuts import render
from .models import Store

def index(request):
    return render(request, 'foods/index.html')

def detail(request):
    # store = Store.objects.get(pk=store_pk)
    # review_form = ReviewForm()
    # context = {'store': store}
    return render(request, 'foods/detail.html')