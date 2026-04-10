from django.contrib import admin
from .models import (
    Lead, CampanhaMarketing, Atendimento, FunilVendas
)

admin.site.register(Lead)
admin.site.register(CampanhaMarketing)
admin.site.register(Atendimento)
admin.site.register(FunilVendas)
