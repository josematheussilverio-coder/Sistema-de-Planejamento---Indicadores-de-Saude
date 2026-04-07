import csv
from datetime import datetime
from django.core.management.base import BaseCommand
from app.models import Cidadao, GrupoRisco 

class Command(BaseCommand):
    help = 'Importa dados dos cidadãos a partir do CSV do e-SUS'

    def add_arguments(self, parser):
        # Permite passar o caminho do arquivo no terminal
        parser.add_argument('csv_file', type=str, help='Caminho para o arquivo CSV')

    def handle(self, *args, **kwargs):
        caminho_arquivo = kwargs['csv_file']
        
        # Função para converter data 'DD/MM/YYYY' para o formato do banco ou retornar Vazio
        def formata_data(data_str):
            if not data_str or data_str == '-':
                return None
            try:
                return datetime.strptime(data_str.strip(), '%d/%m/%Y').date()
            except ValueError:
                return None

        self.stdout.write(self.style.WARNING(f'Lendo o arquivo: {caminho_arquivo}...'))

        # Abre o arquivo com a codificação correta
        # Trocamos utf-8 por latin-1 e tiramos o ignore
        with open(caminho_arquivo, 'r', encoding='latin-1') as f:
            linhas = f.readlines()

        # O e-SUS tem um cabeçalho "sujo" de 20 linhas. Vamos pular até achar a palavra "Nome;"
        inicio_tabela = 0
        for i, linha in enumerate(linhas):
            if linha.startswith('Nome;'):
                inicio_tabela = i
                break

        # Usa o leitor de CSV do Python apontando para a linha certa, separado por ponto e vírgula
        leitor_csv = csv.DictReader(linhas[inicio_tabela:], delimiter=';')
        
        # Garante que o grupo "Diabetes" existe no banco (já que essa planilha é de diabéticos)
        grupo_diabetes, _ = GrupoRisco.objects.get_or_create(nome="Diabetes")
        cadastrados = 0
        atualizados = 0

        for linha in leitor_csv:
            nome = linha.get('Nome', '').strip()
            data_nasc = formata_data(linha.get('Data de nascimento'))
            cns = linha.get('CNS', '').strip()
            
            # Se CNS vier com '-', transforma em None para não dar erro no banco
            if cns == '-': 
                cns = None
            
            # Ignora linhas em branco
            if not nome or not data_nasc:
                continue

            # A MÁGICA DO UPSERT (RF12 - Prevenção de Duplicidade)
            # Ele procura pelo Nome E Data de Nascimento. Se achar, atualiza os defaults. Se não, cria.
            cidadao, criado = Cidadao.objects.update_or_create(
                nome=nome,
                data_nascimento=data_nasc,
                defaults={
                    'cns': cns,
                    'rua': linha.get('Rua', ''),
                    'numero': linha.get('Número', ''),
                    'bairro': linha.get('Bairro', ''),
                    'microarea': str(linha.get('Microárea', '')).zfill(2), # Transforma "4" em "04"
                    
                    # Pegando os dados Clínicos exatos do seu CSV
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
            
            # Adiciona o grupo de risco ao cidadão
            cidadao.grupos_de_risco.add(grupo_diabetes)

            if criado:
                cadastrados += 1
            else:
                atualizados += 1
                
        self.stdout.write(self.style.SUCCESS(f'Sucesso! {cadastrados} novos cadastrados e {atualizados} atualizados.'))