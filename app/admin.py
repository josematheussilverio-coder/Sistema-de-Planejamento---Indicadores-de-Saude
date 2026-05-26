from django.contrib import admin
from .models import Cidadao, GrupoRisco, Consulta, Exame, Vacina, VisitaACS

admin.site.register(GrupoRisco)

class ConsultaInline(admin.TabularInline):
    model = Consulta
    extra = 1

class ExameInline(admin.TabularInline):
    model = Exame
    extra = 1

class VacinaInline(admin.TabularInline):
    model = Vacina
    extra = 1

class VisitaInline(admin.TabularInline):
    model = VisitaACS
    extra = 1

@admin.register(Cidadao)
class CidadaoAdmin(admin.ModelAdmin):
    list_display = ('nome', 'cns', 'microarea', 'bairro')
    search_fields = ('nome', 'cns', 'cpf')
    list_filter = ('grupos_de_risco', 'microarea')
    
    inlines = [ConsultaInline, ExameInline, VacinaInline, VisitaInline]

@admin.register(Consulta)
class ConsultaAdmin(admin.ModelAdmin):
    list_display = ('cidadao', 'tipo', 'data_consulta')
    list_filter = ('tipo', 'data_consulta')
    search_fields = ('cidadao__nome',) 

@admin.register(Exame)
class ExameAdmin(admin.ModelAdmin):
    list_display = ('cidadao', 'tipo', 'data_exame', 'resultado')
    list_filter = ('tipo',)

@admin.register(Vacina)
class VacinaAdmin(admin.ModelAdmin):
    list_display = ('cidadao', 'nome', 'data_aplicacao', 'status')
    list_filter = ('nome', 'status')