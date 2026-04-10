from django.shortcuts import render
def index(request):
    return render(request, 'rh/dashboard.html')
