from django.contrib import admin
from .models import AnoLetivo, MetaInstitucional, ReuniaoEstrategica

@admin.register(AnoLetivo)
class AnoLetivoAdmin(admin.ModelAdmin):
    pass  # Personalize a list_display aqui depois

@admin.register(MetaInstitucional)
class MetaInstitucionalAdmin(admin.ModelAdmin):
    pass  # Personalize a list_display aqui depois

@admin.register(ReuniaoEstrategica)
class ReuniaoEstrategicaAdmin(admin.ModelAdmin):
    pass  # Personalize a list_display aqui depois

