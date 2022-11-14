from django.shortcuts import render, redirect
from .models import Store, Review, ReviewImage, Tag
from .forms import ReviewForm
from django.contrib.auth.decorators import login_required
from articles.models import Stadium, Team
from django.contrib.auth import get_user_model
from django.db.models import Avg


def home(request, team_pk):
    team = Team.objects.get(pk=team_pk)
    stadium = Stadium.objects.get(pk=team.stadium_id)
    stores = Store.objects.filter(team=team)
    context = {
        "team": team,
        "stadium": stadium,
        "stores": stores,
    }
    return render(request, "foods/home.html", context)



def detail(request, team_pk, store_pk):
    team = Team.objects.get(pk=team_pk)
    store = Store.objects.annotate(grade_avg=Avg('store_reviews__grade')).get(pk=store_pk, team=team)
    lat = float(store.lat)
    lon = float(store.lon)
    review_form = ReviewForm()
    context = {'team': team, 'store': store, 'review_form': review_form, 'lat': lat, 'lon': lon}
    return render(request, 'foods/detail.html', context)

@login_required
def create(request, team_pk, store_pk):
    team = Team.objects.get(pk=team_pk)
    store = Store.objects.get(pk=store_pk, team=team)
    if request.method == "POST":
        review_form = ReviewForm(request.POST, request.FILES)
        images = request.FILES.getlist("image")
        if review_form.is_valid():
            review = review_form.save(commit=False)
            review.user = request.user
            review.name = store
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
            return redirect("foods:detail", team.pk, store.pk)
    else:
        review_form = ReviewForm()
    context = {
        "review_form": review_form
    }
    return render(request, "foods/detail.html", context)

@ login_required
def delete(request, team_pk, store_pk, review_pk):
    team = Team.objects.get(pk=team_pk)
    review = Review.objects.get(pk=review_pk)
    store = Store.objects.get(pk=store_pk)
    review.delete()
    return redirect("foods:detail", team.pk, store.pk)

def tag(request, team_pk, tag_pk):
    team = Team.objects.get(pk=team_pk)
    tag = Tag.objects.get(pk=tag_pk)
    store = Store.objects.filter(team=team)
    reviews = []
    for review in tag.tag_articles.all():
        if review.name in store:
            reviews.append(review)
    context={'team': team, 'tag': tag, 'reviews': reviews}
    return render(request, 'foods/tag.html', context)
    