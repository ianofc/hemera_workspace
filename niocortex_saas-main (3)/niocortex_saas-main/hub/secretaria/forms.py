from django import forms
from .models import ModeloDocumento

class ModeloDocumentoForm(forms.ModelForm):
    class Meta:
        model = ModeloDocumento
        fields = ['titulo', 'tipo', 'conteudo']
        widgets = {
            'titulo': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Ex: Declaração de Matrícula 2025'}),
            'tipo': forms.Select(attrs={'class': 'form-select'}),
            'conteudo': forms.Textarea(attrs={'class': 'form-textarea font-mono', 'rows': 15, 'placeholder': 'Ex: Declaramos que o aluno {{ aluno.nome }} está matriculado...'}),
        }