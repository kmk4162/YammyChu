
from django.shortcuts import render, redirect
from .models import Store, Review, ReviewImage
from .forms import ReviewForm
from django.contrib.auth.decorators import login_required
from articles.models import Stadium, Team
from django.contrib.auth import get_user_model


def home(request, team_pk):
    team = Team.objects.get(pk=team_pk)
    stadium = Stadium.objects.get(pk=team.stadium_id)
    context = {
        "team": team,
        "stadium": stadium,
    }
    return render(request, "foods/home.html", context)



def detail(request, store_pk):
    store = Store.objects.get(pk=store_pk)
    review_form = ReviewForm()
    context = {'store': store, 'review_form': review_form}
    return render(request, 'foods/detail.html', context)

@login_required
def create(request, store_pk):
    store = Store.objects.get(pk=store_pk)
    if request.method == "POST":
        review_form = ReviewForm(request.POST, request.FILES)
        images = request.FILES.getlist("image")
        if review_form.is_valid():
            review_form = review_form.save(commit=False)
            review_form.user = request.user
            review_form.name = store
            if len(images):
                for image in images:
                    image_instance = ReviewImage(review=review_form, image=image)
                    review_form.save()
                    image_instance.save()
            else:
                review_form.save()
            return redirect("foods:detail", store.pk)
    else:
        review_form = ReviewForm()
    context = {
        "review_form": review_form
    }
    return render(request, "foods/create.html", context)
