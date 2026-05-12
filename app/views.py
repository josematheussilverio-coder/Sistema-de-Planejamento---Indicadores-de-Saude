from django.shortcuts import render
from django.db.models import Q
from .models import Cidadao, GrupoRisco

def dashboard(request):
    cidadaos = Cidadao.objects.all()
    grupos = GrupoRisco.objects.all()

    termo_busca = request.GET.get('q', '')
    grupo_filtro = request.GET.get('grupo', '')

    if termo_busca:
        cidadaos = cidadaos.filter(
            Q(nome__icontains=termo_busca) | Q(cns__icontains=termo_busca)
        )

    if grupo_filtro:
        cidadaos = cidadaos.filter(grupos_de_risco__nome=grupo_filtro)

    cidadaos = sorted(cidadaos, key=lambda x: x.peso_prioridade)

    contexto = {
        'cidadaos': cidadaos,
        'grupos': grupos,
        'termo_busca': termo_busca,
        'grupo_filtro': grupo_filtro
    }
    
    return render(request, 'dashboard.html', contexto)