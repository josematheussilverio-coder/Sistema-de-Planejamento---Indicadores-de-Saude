from django.contrib import admin
from .models import GrupoRisco, Cidadao

admin.site.register(GrupoRisco)


@admin.register(Cidadao)
class CidadaoAdmin(admin.ModelAdmin):
    list_display = ('nome','cns', 'microarea', 'bairro', 'idade', 'status_consulta_diabetico')

    search_fields = ('nome', 'cns', 'cpf')

    list_filter = ('microarea', 'grupos_de_risco')