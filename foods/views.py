from django.shortcuts import render
from .models import Store

def home(request):
    return render(request, "foods/home.html")

def detail(request):
    # store = Store.objects.get(pk=store_pk)
    # review_form = ReviewForm()
    # context = {'store': store}
    return render(request, 'foods/detail.html')