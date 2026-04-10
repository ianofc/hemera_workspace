from django import forms
from .models import Turma, Aluno, Atividade, Nota, PlanoDeAula, DiarioClasse, Frequencia
from core.models import CustomUser

class TurmaForm(forms.ModelForm):
    class Meta:
        model = Turma
        fields = ['nome', 'ano_letivo', 'periodo']
        widgets = {
            'nome': forms.TextInput(attrs={'class': 'form-input'}),
            'ano_letivo': forms.NumberInput(attrs={'class': 'form-input'}),
            'periodo': forms.TextInput(attrs={'class': 'form-input'}),
        }

class AlunoForm(forms.ModelForm):
    # Campos do User (Nome, Email, etc) não são editados aqui diretamente,
    # mas sim via perfil do usuário. Aqui editamos apenas vínculos escolares.
    
    class Meta:
        model = Aluno
        # [CORREÇÃO] Atualizado de 'matricula_escolar' para 'matricula' para bater com o Model
        fields = ['turma', 'matricula'] 
        widgets = {
            'turma': forms.Select(attrs={'class': 'form-select'}),
            'matricula': forms.TextInput(attrs={'class': 'form-input'}),
        }

class AtividadeForm(forms.ModelForm):
    class Meta:
        model = Atividade
        fields = ['titulo', 'descricao', 'data_entrega', 'disciplina', 'turma']
        widgets = {
            'data_entrega': forms.DateTimeInput(attrs={'type': 'datetime-local', 'class': 'form-input'}),
        }

class NotaForm(forms.ModelForm):
    class Meta:
        model = Nota
        fields = ['aluno', 'atividade', 'valor', 'feedback']

class PlanoDeAulaForm(forms.ModelForm):
    class Meta:
        model = PlanoDeAula
        fields = ['titulo', 'conteudo', 'disciplina', 'data']
        widgets = {
            'data': forms.DateInput(attrs={'type': 'date', 'class': 'form-input'}),
        }

class DiarioClasseForm(forms.ModelForm):
    class Meta:
        model = DiarioClasse
        fields = ['turma', 'disciplina', 'observacoes']
        widgets = {
            'observacoes': forms.Textarea(attrs={'class': 'form-textarea', 'rows': 3}),
        }