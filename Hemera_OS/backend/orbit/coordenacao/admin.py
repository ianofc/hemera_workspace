from django.contrib import admin
from .models import (
    GradeHoraria, PlanejamentoPedagogico, OcorrenciaDisciplinar, ReuniaoPais
)

admin.site.register(GradeHoraria)
admin.site.register(PlanejamentoPedagogico)
admin.site.register(OcorrenciaDisciplinar)
admin.site.register(ReuniaoPais)
