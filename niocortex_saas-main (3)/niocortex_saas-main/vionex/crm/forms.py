from django import forms
from .models import Lead, Oportunidade, FunilEtapa, AtividadeCRM

class LeadForm(forms.ModelForm):
    class Meta:
        model = Lead
        fields = ['nome', 'email', 'telefone', 'origem']
        widgets = {
            'nome': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Nome do Responsável/Aluno'}),
            'email': forms.EmailInput(attrs={'class': 'form-input'}),
            'telefone': forms.TextInput(attrs={'class': 'form-input', 'placeholder': '(00) 00000-0000'}),
            'origem': forms.Select(attrs={'class': 'form-select'}),
        }

class OportunidadeForm(forms.ModelForm):
    class Meta:
        model = Oportunidade
        fields = ['titulo', 'lead', 'etapa', 'valor_estimado', 'probabilidade', 'data_fechamento_prevista']
        widgets = {
            'titulo': forms.TextInput(attrs={'class': 'form-input'}),
            'lead': forms.Select(attrs={'class': 'form-select'}),
            'etapa': forms.Select(attrs={'class': 'form-select'}),
            'valor_estimado': forms.NumberInput(attrs={'class': 'form-input', 'step': '0.01'}),
            'probabilidade': forms.NumberInput(attrs={'class': 'form-input', 'type': 'range', 'min': '0', 'max': '100'}),
            'data_fechamento_prevista': forms.DateInput(attrs={'class': 'form-input', 'type': 'date'}),
        }
    
    def __init__(self, user, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if user and hasattr(user, 'tenant_id'):
            self.fields['lead'].queryset = Lead.objects.filter(tenant_id=user.tenant_id)
            self.fields['etapa'].queryset = FunilEtapa.objects.filter(tenant_id=user.tenant_id).order_by('ordem')

class AtividadeForm(forms.ModelForm):
    class Meta:
        model = AtividadeCRM
        fields = ['tipo', 'descricao']
        widgets = {
            'tipo': forms.Select(attrs={'class': 'form-select'}),
            'descricao': forms.Textarea(attrs={'class': 'form-textarea', 'rows': 3}),
        }