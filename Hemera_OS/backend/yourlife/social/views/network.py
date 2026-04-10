from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required
def network_view(request):
    return render(request, 'social/friends/list.html')
