import csv
from datetime import datetime
from django.core.management.base import BaseCommand
from app.models import Cidadao, GrupoRisco 

class Command(BaseCommand):
    help = 'Importa dados de SAÚDE DA MULHER resolvendo colunas duplicadas do e-SUS'

    def add_arguments(self, parser):
        parser.add_argument('csv_file', type=str, help='Caminho para o arquivo CSV')

    def handle(self, *args, **kwargs):
        caminho_arquivo = kwargs['csv_file']
        
        def formata_data(data_str):
            if not data_str or data_str.strip() == '-':
                return None
            try:
                return datetime.strptime(data_str.strip(), '%d/%m/%Y').date()
            except ValueError:
                return None

        self.stdout.write(self.style.WARNING(f'Lendo o arquivo de mulheres: {caminho_arquivo}...'))

        with open(caminho_arquivo, 'r', encoding='latin-1') as f:
            linhas = f.readlines()

        inicio_tabela = 0
        for i, linha in enumerate(linhas):
            if linha.startswith('Nome;'):
                inicio_tabela = i
                break

        cabecalho = [col.strip() for col in linhas[inicio_tabela].split(';')]
        
        idx_nome = cabecalho.index('Nome')
        idx_nasc = cabecalho.index('Data de nascimento')
        idx_cns = cabecalho.index('CNS')
        idx_rua = cabecalho.index('Rua')
        idx_num = cabecalho.index('Número')
        idx_bairro = cabecalho.index('Bairro')
        idx_micro = cabecalho.index('Microárea')
        
        idx_mamo_sol = cabecalho.index('Exame de rastreamento de câncer de mama data Última solicitação')
        idx_mamo_rea = cabecalho.index('Exame de rastreamento de câncer de mama data Última realização')
        idx_mamo_ava = cabecalho.index('Exame de rastreamento de câncer de mama data Última avaliação')
        
        idx_cito_ava_nome = cabecalho.index('Exame de rastreamento de câncer de colo de útero última avaliação')
        idx_cito_ava_data = cabecalho.index('Exame de rastreamento de câncer de colo de útero data última avaliação')
        
        idx_hpv = cabecalho.index('HPV')

        leitor = csv.reader(linhas[inicio_tabela + 1:], delimiter=';')
        grupo_mulheres, _ = GrupoRisco.objects.get_or_create(nome="Mulheres")
        cadastrados = 0
        atualizados = 0

        for linha in leitor:
            if not linha or len(linha) <= max(idx_nome, idx_nasc):
                continue
                
            nome = linha[idx_nome].strip()
            data_nasc = formata_data(linha[idx_nasc])
            cns = linha[idx_cns].strip()
            if cns == '-': cns = None

            if not nome or not data_nasc:
                continue

            data_mamo = formata_data(linha[idx_mamo_ava])
            status_mamo = "Avaliada"
            if not data_mamo:
                data_mamo = formata_data(linha[idx_mamo_rea])
                status_mamo = "Realizada"
            if not data_mamo:
                data_mamo = formata_data(linha[idx_mamo_sol])
                status_mamo = "Solicitada"
            if not data_mamo:
                status_mamo = "Pendente"

            status_cito_real = linha[idx_cito_ava_nome].strip()
            if status_cito_real == '-': status_cito_real = ""
            
            data_cito_real = formata_data(linha[idx_cito_ava_data])

            try:
                cidadao, criado = Cidadao.objects.update_or_create(
                    nome=nome,
                    data_nascimento=data_nasc,
                    defaults={
                        'cns': cns,
                        'rua': linha[idx_rua],
                        'numero': linha[idx_num],
                        'bairro': linha[idx_bairro],
                        'microarea': str(linha[idx_micro]).zfill(2),
                        
                        'data_exame_citopatologico': data_cito_real,
                        'status_exame_citopatologico': status_cito_real,
                        
                        'data_mamografia': data_mamo,
                        'status_mamografia': status_mamo,
                        
                        'data_vacina_hpv': formata_data(linha[idx_hpv]),
                    }
                )
                
                cidadao.grupos_de_risco.add(grupo_mulheres)
                if criado: cadastrados += 1
                else: atualizados += 1
                    
            except Exception:
                continue

        self.stdout.write(self.style.SUCCESS(f'Sucesso! {cadastrados} novas mulheres cadastradas e {atualizados} atualizadas.'))