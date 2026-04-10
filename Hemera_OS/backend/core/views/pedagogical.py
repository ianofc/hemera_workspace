import json
import mercadopago
from django.conf import settings
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib import messages
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden, JsonResponse
from django.views.decorators.http import require_POST

# --- CORREÇÃO: Importar de ledger.financeiro ---
from ledger.financeiro.models import Transacao
# -----------------------------------------------

from ..forms import CustomUserCreationForm, CustomAuthenticationForm
from ..models import CustomUser
from core.services.ai_client import AIClient

# ==============================================================================
# VIEWS PEDAGÓGICAS (ACADÊMICAS)
# ==============================================================================

# --- Módulos Acadêmicos ---

@login_required
def student_subjects(request):
    """ Lista de Disciplinas """
    is_premium = getattr(request.user, 'is_premium', False)
    return render(request, 'aluno/subjects.html', {'is_premium': is_premium})

@login_required
def student_grades(request):
    """ Boletim e Notas """
    is_premium = getattr(request.user, 'is_premium', False)
    return render(request, 'aluno/grades.html', {'is_premium': is_premium})

@login_required
def student_calendar(request):
    """ Agenda Escolar """
    is_premium = getattr(request.user, 'is_premium', False)
    return render(request, 'aluno/calendar.html', {'is_premium': is_premium})

@login_required
def student_files(request):
    """ Central de Arquivos """
    is_premium = getattr(request.user, 'is_premium', False)
    return render(request, 'aluno/files.html', {'is_premium': is_premium})

@login_required
def student_lesson(request):
    """ Sala de Aula Virtual (Lumenios) """
    is_premium = getattr(request.user, 'is_premium', False)
    return render(request, 'aluno/lesson_viewer.html', {'is_premium': is_premium})

@login_required
def student_activity(request):
    """ Detalhe de Atividade / Entrega """
    is_premium = getattr(request.user, 'is_premium', False)
    return render(request, 'aluno/activity_detail.html', {'is_premium': is_premium})

@login_required
def student_library(request):
    """ Biblioteca Digital e Física """
    is_premium = getattr(request.user, 'is_premium', False)
    return render(request, 'aluno/library.html', {'is_premium': is_premium})

@login_required
def career_center(request):
    """ Portal de Carreiras (Superior/Pós) """
    is_premium = getattr(request.user, 'is_premium', False)
    return render(request, 'aluno/career_center.html', {'is_premium': is_premium})

@login_required
def thesis_manager(request):
    """ Gerenciador de TCC (Superior/Pós) """
    is_premium = getattr(request.user, 'is_premium', False)
    return render(request, 'aluno/thesis_manager.html', {'is_premium': is_premium})

@login_required
def student_timetable(request):
    """ Grade Horária Semanal """
    is_premium = getattr(request.user, 'is_premium', False)
    return render(request, 'aluno/timetable.html', {'is_premium': is_premium})