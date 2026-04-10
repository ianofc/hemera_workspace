from django import forms
from .models import Departamento, Cargo, Funcionario

class DepartamentoForm(forms.ModelForm):
    class Meta:
        model = Departamento
        fields = ['nome', 'codigo_centro_custo', 'responsavel']
        widgets = {
            'nome': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Ex: Secretaria Acadêmica'}),
            'codigo_centro_custo': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'CC-001'}),
            'responsavel': forms.Select(attrs={'class': 'form-select'}),
        }
    
    def __init__(self, user, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if user:
            self.fields['responsavel'].queryset = Funcionario.objects.filter(tenant_id=user.tenant_id)

class CargoForm(forms.ModelForm):
    class Meta:
        model = Cargo
        fields = ['titulo', 'cbo', 'salario_base']
        widgets = {
            'titulo': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Ex: Professor de Matemática'}),
            'cbo': forms.TextInput(attrs={'class': 'form-input', 'placeholder': '0000-00 (Opcional)'}),
            'salario_base': forms.NumberInput(attrs={'class': 'form-input', 'step': '0.01'}),
        }

class FuncionarioForm(forms.ModelForm):
    class Meta:
        model = Funcionario
        fields = [
            'nome_completo', 'cpf', 'rg', 'data_nascimento',
            'cargo', 'departamento', 'matricula', 'tipo_contrato',
            'data_admissao', 'salario_atual',
            'email_corporativo', 'telefone', 'endereco'
        ]
        widgets = {
            'nome_completo': forms.TextInput(attrs={'class': 'form-input'}),
            'cpf': forms.TextInput(attrs={'class': 'form-input', 'placeholder': '000.000.000-00'}),
            'rg': forms.TextInput(attrs={'class': 'form-input'}),
            'data_nascimento': forms.DateInput(attrs={'class': 'form-input', 'type': 'date'}),
            
            'cargo': forms.Select(attrs={'class': 'form-select'}),
            'departamento': forms.Select(attrs={'class': 'form-select'}),
            'matricula': forms.TextInput(attrs={'class': 'form-input'}),
            'tipo_contrato': forms.Select(attrs={'class': 'form-select'}),
            
            'data_admissao': forms.DateInput(attrs={'class': 'form-input', 'type': 'date'}),
            'salario_atual': forms.NumberInput(attrs={'class': 'form-input', 'step': '0.01'}),
            
            'email_corporativo': forms.EmailInput(attrs={'class': 'form-input'}),
            'telefone': forms.TextInput(attrs={'class': 'form-input'}),
            'endereco': forms.Textarea(attrs={'class': 'form-textarea', 'rows': 3}),
        }

    def __init__(self, user, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if user:
            self.fields['cargo'].queryset = Cargo.objects.filter(tenant_id=user.tenant_id)
            self.fields['departamento'].queryset = Departamento.objects.filter(tenant_id=user.tenant_id)