import csv
from datetime import datetime
from django.core.management.base import BaseCommand
from app.models import Cidadao, GrupoRisco 

class Command(BaseCommand):
    help = 'Importa dados dos cidadãos HIPERTENSOS a partir do CSV do e-SUS'

    def add_arguments(self, parser):
        parser.add_argument('csv_file', type=str, help='Caminho para o arquivo CSV de Hipertensos')

    def handle(self, *args, **kwargs):
        caminho_arquivo = kwargs['csv_file']
        
        def formata_data(data_str):
            if not data_str or data_str == '-':
                return None
            try:
                return datetime.strptime(data_str.strip(), '%d/%m/%Y').date()
            except ValueError:
                return None

        self.stdout.write(self.style.WARNING(f'Lendo o arquivo de hipertensos: {caminho_arquivo}...'))

        with open(caminho_arquivo, 'r', encoding='latin-1') as f:
            linhas = f.readlines()

        inicio_tabela = 0
        for i, linha in enumerate(linhas):
            if linha.startswith('Nome;'):
                inicio_tabela = i
                break

        leitor_csv = csv.DictReader(linhas[inicio_tabela:], delimiter=';')
        
        grupo_hipertensao, _ = GrupoRisco.objects.get_or_create(nome="Hipertensão")
        
        cadastrados = 0
        atualizados = 0

        for linha in leitor_csv:
            nome = linha.get('Nome', '').strip()
            data_nasc = formata_data(linha.get('Data de nascimento'))
            cns = linha.get('CNS', '').strip()
            
            if not cns or cns == '-': 
                cns = None
            
            if not nome or not data_nasc:
                continue

            try:
                cidadao, criado = Cidadao.objects.update_or_create(
                    nome=nome,
                    data_nascimento=data_nasc,
                    defaults={
                        'cns': cns,
                        'rua': linha.get('Rua', ''),
                        'numero': linha.get('Número', ''),
                        'bairro': linha.get('Bairro', ''),
                        'microarea': str(linha.get('Microárea', '')).zfill(2),
                        
                        'valor_pa_1': linha.get('Última medição de pressão arterial', ''),
                        'data_pa_1': formata_data(linha.get('Data da última medição de pressão arterial')),
                        
                        'valor_peso_1': linha.get('Última medição de peso', ''),
                        'valor_altura_1': linha.get('Última medição de altura', ''),
                        'data_peso_altura_1': formata_data(linha.get('Data da ultima medição de peso e altura')),
                        
                        'valor_hemoglobina_glicada': linha.get('Hemoglobina glicada', ''),
                        'data_hemoglobina_glicada': formata_data(linha.get('Data da última avaliação de hemoglobina glicada')),
                        
                        'data_avaliacao_pes': formata_data(linha.get('Data da avaliação dos pés')),
                        'data_consulta_1': formata_data(linha.get('Data da última consulta')),
                    }
                )
                
                cidadao.grupos_de_risco.add(grupo_hipertensao)

                if criado:
                    cadastrados += 1
                else:
                    atualizados += 1
                    
            except Exception as e:
                self.stdout.write(self.style.ERROR(f'Aviso: Pulando {nome} devido a conflito de dados (Ex: CNS já cadastrado em outro nome).'))
                continue