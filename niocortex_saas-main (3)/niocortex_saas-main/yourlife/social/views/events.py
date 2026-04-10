from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required
def events_list_view(request):
    # Lista de eventos próximos (estilo Eventbrite / Facebook Events)
    return render(request, 'social/events/list.html')

@login_required
def event_detail_view(request, event_id):
    return render(request, 'social/events/detail.html')

@login_required
def calendar_view(request):
    return render(request, 'social/events/calendar.html')
