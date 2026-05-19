from django.shortcuts import render, redirect
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.core.management import call_command
from django.core.files.storage import FileSystemStorage
from django.contrib import messages
from .models import Cidadao, GrupoRisco
import os

@login_required
def dashboard(request):
    termo_busca = request.GET.get('q', '')

@login_required
def importar_planilhas(request):
    if not request.user.is_superuser:
        return redirect('dashboard')

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

@login_required
def dashboard(request):
    termo_busca = request.GET.get('q', '')
    grupo_filtro = request.GET.get('grupo', '')

    cidadaos = Cidadao.objects.all()

    if termo_busca:
        cidadaos = cidadaos.filter(
            Q(nome__icontains=termo_busca) |
            Q(cns__icontains=termo_busca) |
            Q(rua__icontains=termo_busca) |
            Q(bairro__icontains=termo_busca)
        )

    if grupo_filtro:
        cidadaos = cidadaos.filter(grupos_de_risco__nome=grupo_filtro)

    for cidadao in cidadaos:
        indicadores = []
        grupos_do_cidadao = [g.nome for g in cidadao.grupos_de_risco.all()]

        if grupo_filtro == 'Diabetes':
            indicadores.append(cidadao.status_consulta_diabetico)
        elif grupo_filtro == 'Hipertensão':
            indicadores.append(cidadao.status_consulta_hipertenso)
        elif grupo_filtro == 'Idoso':
            indicadores.append(cidadao.status_consulta_idoso)
        elif grupo_filtro == 'Gestante':
            indicadores.extend([cidadao.status_pre_natal, cidadao.status_vacina_dtpa, cidadao.status_testes_gestante])
        elif grupo_filtro == 'Criança':
            indicadores.extend([cidadao.status_consultas_crianca, cidadao.status_vacinas_crianca])
        elif grupo_filtro == 'Mulheres':
            indicadores.extend([cidadao.status_citopatologico, cidadao.status_mamografia_farol])
        else:
            if "Diabetes" in grupos_do_cidadao: indicadores.append(cidadao.status_consulta_diabetico)
            if "Hipertensão" in grupos_do_cidadao: indicadores.append(cidadao.status_consulta_hipertenso)
            if "Idoso" in grupos_do_cidadao: indicadores.append(cidadao.status_consulta_idoso)
            if "Gestante" in grupos_do_cidadao: indicadores.extend([cidadao.status_pre_natal, cidadao.status_vacina_dtpa, cidadao.status_testes_gestante])
            if "Criança" in grupos_do_cidadao: indicadores.extend([cidadao.status_consultas_crianca, cidadao.status_vacinas_crianca])
            if "Mulheres" in grupos_do_cidadao: indicadores.extend([cidadao.status_citopatologico, cidadao.status_mamografia_farol])

        if not indicadores:
            cidadao.cor_dinamica = "secondary"
            cidadao.peso_dinamico = 4
        elif any("🔴" in status for status in indicadores):
            cidadao.cor_dinamica = "danger"
            cidadao.peso_dinamico = 1
        elif any("🟡" in status for status in indicadores):
            cidadao.cor_dinamica = "warning"
            cidadao.peso_dinamico = 2
        else:
            cidadao.cor_dinamica = "success"
            cidadao.peso_dinamico = 3

    cidadaos_ordenados = sorted(cidadaos, key=lambda x: x.peso_dinamico)

    total_pacientes = len(cidadaos_ordenados)
    total_criticos = sum(1 for c in cidadaos_ordenados if c.peso_dinamico == 1)
    total_atencao = sum(1 for c in cidadaos_ordenados if c.peso_dinamico == 2)
    total_em_dia = sum(1 for c in cidadaos_ordenados if c.peso_dinamico == 3)

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