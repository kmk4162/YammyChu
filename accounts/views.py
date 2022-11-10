from django.shortcuts import render
from .models import User

def profile(request, pk):
    user = User.objects.get(pk=pk)
    print(user.nickname)
    context = {
        'pk': pk,
        'nickname': user.nickname,
    }
    return render(request, 'accounts/profile.html', context)