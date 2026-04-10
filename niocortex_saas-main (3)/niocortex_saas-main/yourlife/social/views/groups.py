from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

@login_required
def groups_list_view(request):
    # Renderiza a lista de comunidades (estilo Facebook Groups / Reddit)
    return render(request, 'social/groups/list.html')

@login_required
def group_detail_view(request, group_id):
    # Renderiza a home de um grupo específico
    return render(request, 'social/groups/detail.html')

@login_required
def group_create_view(request):
    return render(request, 'social/groups/create.html')
