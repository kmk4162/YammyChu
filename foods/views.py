from django.shortcuts import render
from .models import Store
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


def detail(request):
    # store = Store.objects.get(pk=store_pk)
    # review_form = ReviewForm()
    # context = {'store': store}
    return render(request, "foods/detail.html")
