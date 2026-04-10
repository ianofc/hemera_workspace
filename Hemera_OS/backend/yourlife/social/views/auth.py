from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm

def login_view(request):
    if request.user.is_authenticated:
        return redirect('yourlife_social:home')
        
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('yourlife_social:home')
    else:
        form = AuthenticationForm()
    return render(request, 'social/auth/login.html', {'form': form})

def register_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('yourlife_social:home')
    else:
        form = UserCreationForm()
    return render(request, 'social/auth/register.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('yourlife_social:login')
