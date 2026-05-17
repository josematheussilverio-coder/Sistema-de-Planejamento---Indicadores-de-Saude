import csv
from datetime import datetime
from django.core.management.base import BaseCommand
from app.models import Cidadao, GrupoRisco 

class Command(BaseCommand):
    help = 'Importa dados de CRIANÇAS a partir do CSV do e-SUS'

    def add_arguments(self, parser):
        parser.add_argument('csv_file', type=str, help='Caminho para o arquivo CSV de Crianças')

    def handle(self, *args, **kwargs):
        caminho_arquivo = kwargs['csv_file']
        
        def formata_data(data_str):
            if not data_str or data_str == '-':
                return None
            try:
                return datetime.strptime(data_str.strip(), '%d/%m/%Y').date()
            except ValueError:
                return None

        def formata_inteiro(valor_str):
            if not valor_str or valor_str.strip() == '-' or valor_str.strip() == '':
                return 0
            try:
                return int(valor_str.strip())
            except ValueError:
                return 0

        self.stdout.write(self.style.WARNING(f'Lendo o arquivo de crianças: {caminho_arquivo}...'))

        with open(caminho_arquivo, 'r', encoding='latin-1') as f:
            linhas = f.readlines()

        inicio_tabela = 0
        for i, linha in enumerate(linhas):
            if linha.startswith('Nome;'):
                inicio_tabela = i
                break

        leitor_csv = csv.DictReader(linhas[inicio_tabela:], delimiter=';')
        
        grupo_crianca, _ = GrupoRisco.objects.get_or_create(nome="Criança")
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
                        
                        'qtd_consultas_crianca': formata_inteiro(linha.get('Quantidade de consultas até 24 meses')),

                        'info_vacina_pentavalente': linha.get('Difteria, Tétano, Pertusis, Hepatite B, Haemophilus, Influenza B', ''),
                        'info_vacina_triplice_viral': linha.get('Sarampo, Caxumba, Rubéola', ''),
                        'info_vacina_polio': linha.get('Poliomielite', ''),
                        'info_vacina_pneumo': linha.get('Pneumocócica', ''),
                    }
                )
                
                cidadao.grupos_de_risco.add(grupo_crianca)

                if criado:
                    cadastrados += 1
                else:
                    atualizados += 1
                    
            except Exception as e:
                self.stdout.write(self.style.ERROR(f'Aviso: Pulando {nome} devido a conflito de dados.'))
                continue
                
        self.stdout.write(self.style.SUCCESS(f'Sucesso! {cadastrados} novas crianças cadastradas e {atualizados} atualizadas.'))