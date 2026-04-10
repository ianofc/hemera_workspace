from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ['username', 'role', 'nivel_ensino', 'is_staff']
    fieldsets = UserAdmin.fieldsets + (
        ('NioCortex', {'fields': ('role', 'avatar', 'bio', 'cpf')}),
        ('Contexto', {'fields': ('nivel_ensino', 'tenant_type', 'school', 'turma')}),
    )