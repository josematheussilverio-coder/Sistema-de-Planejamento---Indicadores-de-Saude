import os
from django.shortcuts import render, redirect
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.core.management import call_command          
from django.core.files.storage import FileSystemStorage  
from django.contrib import messages                      
from .models import Cidadao, GrupoRisco

@login_required 
def dashboard(request):
    termo_busca = request.GET.get('q', '')

@login_required
def importar_planilhas(request):
    if request.method == 'POST' and request.FILES.get('arquivo_csv'):
        arquivo = request.FILES['arquivo_csv']
        tipo_importacao = request.POST.get('tipo_importacao')

        fs = FileSystemStorage()
        filename = fs.save(arquivo.name, arquivo)
        caminho_arquivo = fs.path(filename)

        try:
            comandos = {
                'diabeticos': 'importar_csv', 
                'hipertensos': 'importar_hipertensos',
                'gestantes': 'importar_gestantes',
                'idosos': 'importar_idosos',
                'criancas': 'importar_criancas',
                'mulheres': 'importar_mulheres',
            }

            comando_escolhido = comandos.get(tipo_importacao)
            
            if comando_escolhido:
                call_command(comando_escolhido, caminho_arquivo)
                messages.success(request, 'Planilha processada com sucesso! Os dados foram atualizados.')
            else:
                messages.error(request, 'Tipo de grupo inválido.')

        except Exception as e:
            messages.error(request, f'Erro ao processar o arquivo. Verifique se escolheu o grupo certo. Detalhe: {e}')
        
        finally:
            if os.path.exists(caminho_arquivo):
                os.remove(caminho_arquivo)

        return redirect('dashboard')

    return render(request, 'upload.html')

def dashboard(request):
    termo_busca = request.GET.get('q', '')
    grupo_filtro = request.GET.get('grupo', '')

    cidadaos = Cidadao.objects.all()

    if termo_busca:
        cidadaos = cidadaos.filter(
            Q(nome__icontains=termo_busca) | Q(cns__icontains=termo_busca)
        )

    if grupo_filtro:
        cidadaos = cidadaos.filter(grupos_de_risco__nome=grupo_filtro)

    cidadaos_ordenados = sorted(cidadaos, key=lambda x: x.peso_prioridade)

    total_pacientes = len(cidadaos_ordenados)
    total_criticos = sum(1 for c in cidadaos_ordenados if c.peso_prioridade == 1)
    total_atencao = sum(1 for c in cidadaos_ordenados if c.peso_prioridade == 2)
    total_em_dia = sum(1 for c in cidadaos_ordenados if c.peso_prioridade == 3)

    grupos = GrupoRisco.objects.all()

    contexto = {
        'cidadaos': cidadaos_ordenados,
        'grupos': grupos,
        'termo_busca': termo_busca,
        'grupo_filtro': grupo_filtro,
        'total_pacientes': total_pacientes,
        'total_criticos': total_criticos,
        'total_atencao': total_atencao,
        'total_em_dia': total_em_dia,
    }
    
    return render(request, 'dashboard.html', contexto)