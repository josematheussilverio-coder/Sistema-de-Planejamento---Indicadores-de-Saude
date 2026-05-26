from django.db import models

class GrupoRisco(models.Model):
    nome = models.CharField(max_length=100)
    def __str__(self):
        return self.nome

class Cidadao(models.Model):
    nome = models.CharField(max_length=200)
    cpf = models.CharField(max_length=14, blank=True, null=True)
    cns = models.CharField(max_length=15, unique=True)
    data_nascimento = models.DateField()
    rua = models.CharField(max_length=200)
    numero = models.CharField(max_length=20, blank=True, null=True)
    bairro = models.CharField(max_length=100)
    microarea = models.CharField(max_length=10)
    SEXO_CHOICES = [('M', 'Masculino'), ('F', 'Feminino')]
    sexo = models.CharField(max_length=1, choices=SEXO_CHOICES, default='F')
    
    grupos_de_risco = models.ManyToManyField(GrupoRisco, blank=True)
    dum = models.DateField("Data da Última Menstruação (DUM)", blank=True, null=True)
    dpp = models.DateField("Data Provável do Parto (DPP)", blank=True, null=True)

    def __str__(self):
        return self.nome

class Consulta(models.Model):
    TIPOS_CONSULTA = [
        ('Medica', 'Consulta Médica'),
        ('PreNatal', 'Consulta Pre-Natal'),
        ('Puericultura', 'Puericultura'),
        ('Odonto', 'Odontológica'),
        ('Enfermagem', 'Enfermagem'),
        ('Puerperio','Consulta de Puerperio')
        ('SaudeSexual', 'Saúde Sexual e Reprodutiva')
    ]
    cidadao = models.ForeignKey(Cidadao, on_delete=models.CASCADE, related_name='consultas')
    data_consulta = models.DateField()
    tipo = models.CharField(max_length=50, choices=TIPOS_CONSULTA)
    
    def __str__(self):
        return f"{self.tipo} - {self.cidadao.nome} ({self.data_consulta})"

class Exame(models.Model):
    TIPOS_EXAME = [
        ('Pressao', 'Aferição de Pressão Arterial'),
        ('PesoAltura', 'Medição de Peso e Altura'),
        ('Hemoglobina', 'Hemoglobina Glicada'),
        ('Pes', 'Avaliação dos Pés (Diabético)'),
        ('Citopatologico', 'Citopatológico (Preventivo)'),
        ('Mamografia', 'Mamografia'),
        ('TesteRapido', 'Teste Rápido (Sífilis/HIV)'),
    ]
    cidadao = models.ForeignKey(Cidadao, on_delete=models.CASCADE, related_name='exames')
    tipo = models.CharField(max_length=50, choices=TIPOS_EXAME)
    data_exame = models.DateField()
    resultado = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return f"{self.tipo} - {self.cidadao.nome} ({self.data_exame})"

class Vacina(models.Model):
    NOME_VACINAS = [
        ('Influenza', 'Influenza'),
        ('dTpa', 'dTpa (Gestante)'),
        ('Pentavalente', 'Pentavalente'),
        ('Polio', 'Poliomielite'),
        ('Pneumo', 'Pneumocócica'),
        ('HPV', 'HPV'),
        ('TripliceViral', 'Triplice Viral (SCR)')
    ]
    cidadao = models.ForeignKey(Cidadao, on_delete=models.CASCADE, related_name='vacinas')
    nome = models.CharField(max_length=50, choices=NOME_VACINAS)
    data_aplicacao = models.DateField(blank=True, null=True)
    status = models.CharField(max_length=50, default="Realizada") # Ex: Atrasada, Realizada

    def __str__(self):
        return f"{self.nome} - {self.cidadao.nome}"

class VisitaACS(models.Model):
    cidadao = models.ForeignKey(Cidadao, on_delete=models.CASCADE, related_name='visitas')
    data_visita = models.DateField()
    
    def __str__(self):
        return f"Visita em {self.data_visita} - {self.cidadao.nome}"