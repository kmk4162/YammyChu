from django.shortcuts import render, redirect
from .models import Store, Review, ReviewImage, Tag, RestaurantImage, Restaurant
from .forms import ReviewForm, ReviewImageForm, RestaurantForm, RestaurantImageForm
from django.contrib.auth.decorators import login_required
from articles.models import Stadium, Team
from django.contrib.auth import get_user_model
from django.db.models import Avg
from django.contrib import messages


def home(request, team_pk):
    team = Team.objects.get(pk=team_pk)
    stadium = Stadium.objects.get(pk=team.stadium_id)
    stores = Store.objects.filter(team=team)
    restaurants = Restaurant.objects.filter(team=team)
    context = {
        "team": team,
        "stadium": stadium,
        "stores": stores,
        'restaurants': restaurants,
    }
    return render(request, "foods/home.html", context)

def store_detail(request, team_pk, store_pk):
    team = Team.objects.get(pk=team_pk)
    store = Store.objects.annotate(grade_avg=Avg('store_reviews__grade')).get(pk=store_pk, team=team)
    lat = float(store.lat)
    lon = float(store.lon)
    review_form = ReviewForm()
    reviewimage_form = ReviewImageForm()
    context = {'team': team, 'store': store, 'review_form': review_form, 'reviewimage_form': reviewimage_form, 'lat': lat, 'lon': lon}
    return render(request, 'foods/store_detail.html', context)

@login_required
def store_review_create(request, team_pk, store_pk):
    team = Team.objects.get(pk=team_pk)
    store = Store.objects.get(pk=store_pk, team=team)
    if request.method == "POST":
        review_form = ReviewForm(request.POST, request.FILES)
        reviewimage_form = ReviewImageForm(request.POST, request.FILES)
        images = request.FILES.getlist("image")
        if review_form.is_valid() and reviewimage_form.is_valid():
            review = review_form.save(commit=False)
            review.user = request.user
            review.store_name = store
            if len(images):
                for image in images:
                    image_instance = ReviewImage(review=review, image=image)
                    review.save()
                    image_instance.save()
            else:
                review.save()
            for word in review.content.split():
                if word.startswith('#'):
                    tag, created = Tag.objects.get_or_create(content=word)
                    review.tags.add(tag)
            return redirect("foods:store_detail", team.pk, store.pk)
    else:
        review_form = ReviewForm()
        reviewimage_form = ReviewImageForm()
    context = {
        "review_form": review_form, 
        "reviewimage_form": reviewimage_form
    }
    return render(request, "foods/store_detail.html", context)

@ login_required
def store_review_delete(request, team_pk, store_pk, review_pk):
    team = Team.objects.get(pk=team_pk)
    review = Review.objects.get(pk=review_pk)
    store = Store.objects.get(pk=store_pk)
    review.delete()
    return redirect("foods:store_detail", team.pk, store.pk)

def restaurant_detail(request, team_pk, restaurant_pk):
    team = Team.objects.get(pk=team_pk)
    restaurant = Restaurant.objects.annotate(grade_avg=Avg('restaurant_reviews__grade')).get(pk=restaurant_pk, team=team)
    lat = float(restaurant.lat)
    lon = float(restaurant.lon)
    review_form = ReviewForm()
    reviewimage_form = ReviewImageForm()
    context = {'team': team, 'restaurant': restaurant, 'review_form': review_form, 'reviewimage_form': reviewimage_form, 'lat': lat, 'lon': lon}
    return render(request, 'foods/restaurant_detail.html', context)

# restaurant를 유저가 직접 쓸 수 있게 하는 페이지, update와 delete는 관리자 권한으로
@login_required
def restaurant_create(request, team_pk):
    team = Team.objects.get(pk=team_pk)
    if request.method == "POST":
        restaurant_form = RestaurantForm(request.POST, request.FILES)
        restaurantimage_form = RestaurantImageForm(request.POST, request.FILES)
        images = request.FILES.getlist("image")
        if restaurant_form.is_valid() and restaurantimage_form.is_valid():
            restaurant = restaurant_form.save(commit=False)
            restaurant.team = team
            if len(images):
                for image in images:
                    image_instance = RestaurantImage(restaurant=restaurant, image=image)
                    restaurant.save()
                    image_instance.save()
            else:
                restaurant.save()
            return redirect("foods:restaurant_detail", team.pk, restaurant.pk)
    else:
        restaurant_form = RestaurantForm()
        restaurantimage_form = RestaurantImageForm()
    context = {
        "restaurant_form": restaurant_form, 
        "restaurantimage_form": restaurantimage_form,
        'team': team,
    }
    return render(request, "foods/restaurant_create.html", context)

@login_required
def restaurant_review_create(request, team_pk, restaurant_pk):
    team = Team.objects.get(pk=team_pk)
    restaurant = Restaurant.objects.get(pk=restaurant_pk, team=team)
    if request.method == "POST":
        review_form = ReviewForm(request.POST, request.FILES)
        reviewimage_form = ReviewImageForm(request.POST, request.FILES)
        images = request.FILES.getlist("image")
        if review_form.is_valid() and reviewimage_form.is_valid():
            review = review_form.save(commit=False)
            review.user = request.user
            review.restaurant_name = restaurant
            if len(images):
                for image in images:
                    image_instance = ReviewImage(review=review, image=image)
                    review.save()
                    image_instance.save()
            else:
                review.save()
            for word in review.content.split():
                if word.startswith('#'):
                    tag, created = Tag.objects.get_or_create(content=word)
                    review.tags.add(tag)
            return redirect("foods:restaurant_detail", team.pk, restaurant.pk)
    else:
        review_form = ReviewForm()
        reviewimage_form = ReviewImageForm()
    context = {
        "review_form": review_form, 
        "reviewimage_form": reviewimage_form
    }
    return render(request, "foods/restaurant_detail.html", context)

@ login_required
def restaurant_review_delete(request, team_pk, restaurant_pk, review_pk):
    team = Team.objects.get(pk=team_pk)
    review = Review.objects.get(pk=review_pk)
    restaurant = Restaurant.objects.get(pk=restaurant_pk)
    review.delete()
    return redirect("foods:restaurant_detail", team.pk, restaurant.pk)

# store과 restaurant의 태그를 모두 아우름
# 아예 그냥 store과 restaurant를 반으로 나눌까
def tag(request, team_pk, tag_pk):
    team = Team.objects.get(pk=team_pk)
    tag = Tag.objects.get(pk=tag_pk)
    store = Store.objects.filter(team=team)
    restaurant = Restaurant.objects.filter(team=team)
    reviews = []
    for review in tag.tag_articles.all():
        if review.store_name in store:
            reviews.append(review)
    for review in tag.tag_articles.all():
        if review.restaurant_name in restaurant:
            reviews.append(review)
    context={'team': team, 'tag': tag, 'reviews': reviews}
    return render(request, 'foods/tag.html', context)
    