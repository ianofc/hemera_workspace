# niocortex_saas/core/forms.py

from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import CustomUser
from uuid import uuid4

FREEMIUM_ROLES = [
    ('PROFESSOR_FREE', 'Professor (Gestão de Turmas - Limite 20 Alunos)'),
    ('ALUNO_FREE', 'Aluno (Homeschooling/Autoestudo - Acesso Vitalício)'),
]

class CustomUserCreationForm(UserCreationForm):
    role_initial = forms.ChoiceField(
        choices=FREEMIUM_ROLES,
        label="Eu sou...",
        widget=forms.RadioSelect,
        initial='PROFESSOR_FREE'
    )
    
    email = forms.EmailField(required=True, label="E-mail")

    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = UserCreationForm.Meta.fields + ('email', 'role_initial',)
        
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if CustomUser.objects.filter(email=email).exists():
            raise forms.ValidationError("Este endereço de e-mail já está em uso.")
        return email

    def save(self, commit=True):
        user = super().save(commit=False)
        
        # 1. Atribui a Role e define como Usuário Individual
        user.role = self.cleaned_data.get('role_initial')
        user.tenant_type = 'INDIVIDUAL'
        
        # 2. Gera o tenant_id ANTES de salvar no banco
        if not user.tenant_id:
            user.tenant_id = uuid4()
            
        if commit:
            user.save()
            
        return user

class CustomAuthenticationForm(AuthenticationForm):
    pass