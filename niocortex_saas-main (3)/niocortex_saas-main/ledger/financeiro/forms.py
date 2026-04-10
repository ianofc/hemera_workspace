from django import forms
from .models import ContratoAluno, Fornecedor, Patrimonio
from lumenios.pedagogico.models import Aluno

# --- GESTÃO DE COMPRAS E PATRIMÓNIO ---

class FornecedorForm(forms.ModelForm):
    class Meta:
        model = Fornecedor
        fields = ['razao_social', 'cnpj', 'categoria', 'telefone', 'aprovado_licitacao']
        widgets = {
            'razao_social': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Nome da Empresa'}),
            'cnpj': forms.TextInput(attrs={'class': 'form-input', 'placeholder': '00.000.000/0000-00'}),
            'categoria': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Ex: Informática, Limpeza'}),
            'telefone': forms.TextInput(attrs={'class': 'form-input'}),
            'aprovado_licitacao': forms.CheckboxInput(attrs={'class': 'form-checkbox h-5 w-5 text-[#6200EA]'}),
        }

class PatrimonioForm(forms.ModelForm):
    class Meta:
        model = Patrimonio
        fields = ['codigo_etiqueta', 'descricao', 'data_aquisicao', 'valor_compra', 'vida_util_anos', 'estado_conservacao']
        widgets = {
            'codigo_etiqueta': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'ETQ-00001'}),
            'descricao': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Ex: Projetor Epson X50'}),
            'data_aquisicao': forms.DateInput(attrs={'type': 'date', 'class': 'form-input'}),
            'valor_compra': forms.NumberInput(attrs={'class': 'form-input', 'step': '0.01'}),
            'vida_util_anos': forms.NumberInput(attrs={'class': 'form-input'}),
            'estado_conservacao': forms.Select(attrs={'class': 'form-select'}),
        }

class ContratoAlunoForm(forms.ModelForm):
    class Meta:
        model = ContratoAluno
        fields = [
            'aluno', 
            'responsavel_financeiro', 'cpf_cnpj_responsavel',
            'valor_mensalidade', 'dia_vencimento'
        ]
        widgets = {
            'aluno': forms.Select(attrs={'class': 'form-select'}),
            'responsavel_financeiro': forms.TextInput(attrs={'class': 'form-input'}),
            'cpf_cnpj_responsavel': forms.TextInput(attrs={'class': 'form-input'}),
            'valor_mensalidade': forms.NumberInput(attrs={'class': 'form-input', 'step': '0.01'}),
            'dia_vencimento': forms.NumberInput(attrs={'class': 'form-input', 'min': 1, 'max': 31}),
        }

    def __init__(self, user, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if user:
            self.fields['aluno'].queryset = Aluno.objects.filter(tenant_id=user.tenant_id).order_by('nome')

class GerarBoletoForm(forms.Form):
    referencia = forms.CharField(
        label="Referência / Descrição",
        max_length=50,
        widget=forms.TextInput(attrs={'class': 'form-input'})
    )
    valor = forms.DecimalField(
        label="Valor (R$)",
        max_digits=10, 
        decimal_places=2,
        required=False,
        widget=forms.NumberInput(attrs={'class': 'form-input'})
    )