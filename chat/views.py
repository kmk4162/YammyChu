from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from articles.models import Team


@login_required
def index(request):

    return render(request, 'chat/index.html')


@login_required
def room(request, room_name):
    team = Team.objects.get(ename=room_name)
    context = {
        "room_name": room_name,
        "team": team,
    }
    return render(request, "chat/room.html", context)