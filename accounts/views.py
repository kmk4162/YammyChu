from .models import User
from django.shortcuts import render, redirect
from .forms import CustomUserCreationForm, CustomUserChangeForm
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm
from django.contrib import messages
from django.contrib.auth import (
    login as auth_login,
    logout as auth_logout,
)
from django.contrib.auth.decorators import login_required
from articles.models import Team
from django.http import JsonResponse, QueryDict
from django.views.decorators.http import require_http_methods, require_POST, require_safe

def signup(request):
    teams = Team.objects.all()
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.team = Team.objects.get(pk=int(request.POST.get("team")))
            user.save()
            auth_login(request, user)
            return redirect("articles:index")
    else:
        form = CustomUserCreationForm()
    context = {
        "form": form,
        "teams":teams,
    }
    return render(request, "accounts/signup.html", context)

def login(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            auth_login(request, form.get_user())
            messages.success(request, "로그인 되었습니다.")
            return redirect("articles:index")
    else:
        form = AuthenticationForm()
    context = {
        "form": form,
    }
    return render(request, "accounts/login.html", context)

@login_required
def logout(request):
    auth_logout(request)
    messages.success(request, "로그아웃 되었습니다.")
    return redirect("articles:index")

def profile(request, pk):
    user = User.objects.get(pk=pk)
    if user.team :
        team = Team.objects.get(pk=user.team_id)
        context = {
            'team': team,
            'request_user': user,
            'pk': pk,
            'username': user.username,
            'email': user.email,
            'name': user.last_name,
            'nickname': user.nickname,
        }
    else :
        context = {
            'request_user': user,
            'pk': pk,
            'username': user.username,
            'email': user.email,
            'name': user.last_name,
            'nickname': user.nickname,
        }
    return render(request, 'accounts/profile.html', context)

@require_POST
def follow(request, pk):
    if request.user.is_authenticated:
        user = User.objects.get(pk=pk)
        if user != request.user:
            if user.followers.filter(pk=request.user.pk).exists():
                user.followers.remove(request.user)
                is_followed = False
            else:
                user.followers.add(request.user)
                is_followed = True
            follow_user = user.followers.filter(pk=request.user.pk)
            following_user = user.followings.filter(pk=request.user.pk)
            print(follow_user)
            follow_user_list = []
            following_user_list = []
            for follow in follow_user:
                follow_user_list.append({'pk': follow.pk, 'username': follow.username,})
            for following in following_user:
                following_user_list.append({'pk': following.pk, 'username': following.username,})
            print("팔로우됨?")
            context = {
                'is_followed': is_followed,
                'follow_user': follow_user_list,
                'following_user': following_user_list,
                'followers_count': user.followers.count(),
                'followings_count': user.followings.count(),
            }
            return JsonResponse(context)
        return redirect('accounts:profile', user.pk)
    return redirect('accounts:login')

@require_POST
def update(request):
    teams = Team.objects.all()
    user = User.objects.get(pk=request.user.pk)
    if request.method == 'POST':
        if request.user.is_authenticated:
            form = CustomUserChangeForm(data=request.POST, instance=request.user)
            if form.is_valid():
                user = form.save(commit=False)
                user.team = Team.objects.get(pk=int(request.POST.get("team")))
                user.save()
                return redirect('accounts:profile', request.user.pk)
    else:
        form = CustomUserChangeForm(instance=user)
    context = {
        'form': form,
        "teams":teams,
    }
    return render(request, 'accounts/update.html', context)

@login_required
def password(request):
    if request.method == 'POST' :
        if request.user.is_authenticated:
            form = PasswordChangeForm(request.user, request.POST)
            if form.is_valid():
                user = form.save()
                auth_login(request, user)
                return redirect('accounts:profile', request.user.pk)
    else:
        form = PasswordChangeForm(request.user)
    context = {
        'form': form,
    }
    return render(request, 'accounts/password.html', context)

def delete(request):
    request.user.delete()
    auth_logout(request)
    return redirect('articles:index')