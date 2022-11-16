from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from articles.models import Team
from django.utils.safestring import mark_safe
import json


@login_required
def index(request):

    return render(request, 'chat/index.html')


@login_required
def room(request, room_name):
    team = Team.objects.get(ename=room_name)
    team_img = Team.objects.get(pk=request.user.team_id).logo.url
    context = {
        "room_name": room_name,
        "team": team,
        "team_img": mark_safe(json.dumps(team_img)),
        "user_pk": request.user.pk,
        "username": request.user.nickname,
    }
    return render(request, "chat/room.html", context)