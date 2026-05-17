from django.db import models
from datetime import date

class GrupoRisco(models.Model):
    nome = models.CharField(max_length=50, unique=True, verbose_name="Nome do Grupo")

    def __str__(self):
        return self.nome
    
    class Meta:
        verbose_name = "Grupo de Risco"
        verbose_name_plural = "Grupos de Risco"


class Cidadao(models.Model):

    nome = models.CharField(max_length=200, verbose_name="Nome do Cidadão")
    cpf = models.CharField(max_length=14, blank=True, null=True, unique=True, verbose_name="CPF")
    cns = models.CharField(max_length=20, blank=True, null=True, unique=True, verbose_name="CNS")
    data_nascimento = models.DateField(verbose_name="Data de Nascimento")

    rua = models.CharField(max_length=200, verbose_name="Rua")
    numero = models.CharField(max_length=20, blank=True, null=True, verbose_name="Número")
    bairro= models.CharField(max_length=100, verbose_name="Bairro")
    microarea = models.CharField(max_length=10, verbose_name="Microárea")

    grupos_de_risco = models.ManyToManyField(GrupoRisco, blank=True, verbose_name="Grupos de Risco")

    data_consulta_1 = models.DateField(blank=True, null=True, verbose_name="Primeira Consulta")
    data_consulta_2 = models.DateField(blank=True, null=True, verbose_name="Segunda Consulta")

    data_visita_1 = models.DateField(blank=True, null=True, verbose_name="Visita Domiciliar 1")
    data_visita_2 = models.DateField(blank=True, null=True, verbose_name="Visita Domiciliar 2")

    data_pa_1 = models.DateField(blank=True, null=True, verbose_name="Data P.A. 1")
    valor_pa_1 = models.CharField(max_length=20, blank=True, null=True, verbose_name="Valor P.A. 1")
    data_pa_2 = models.DateField(blank=True, null=True, verbose_name="Data P.A. 2")
    valor_pa_2 = models.CharField(max_length=20, blank=True, null=True, verbose_name="Valor P.A. 2")

    data_peso_altura_1 = models.DateField(blank=True, null=True, verbose_name="Data Peso/Altura 1")
    valor_peso_1 = models.CharField(max_length=10, blank=True, null=True, verbose_name="Valor Peso 1")
    valor_altura_1 = models.CharField(max_length=10, blank=True, null=True, verbose_name="Valor Altura 1")

    data_peso_altura_2 = models.DateField(blank=True, null=True, verbose_name="Data Peso/Altura 2")
    valor_peso_2 = models.CharField(max_length=10, blank=True, null=True, verbose_name="Valor Peso 2")
    valor_altura_2 = models.CharField(max_length=10, blank=True, null=True, verbose_name="Valor Altura 2")

    #diabetes
    data_hemoglobina_glicada = models.DateField(blank=True, null=True, verbose_name="Hemoglobina Glicada")
    valor_hemoglobina_glicada = models.CharField(max_length=20, blank=True, null=True, verbose_name="Valor Hemoglobina Glicada")
    data_avaliacao_pes = models.DateField(blank=True, null=True, verbose_name="Avaliação do Pés")

    #gestantes
    dum = models.DateField(blank=True, null=True, verbose_name="DUM (Data da Última Menstruação)")
    dpp = models.DateField(blank=True, null=True, verbose_name="DPP (Data do Provável Parto)")
    qtde_consultas_pre_natal = models.IntegerField(default=0, verbose_name="Nº de Consulta Pré-Natal")
    qtd_visitas_gestante = models.IntegerField(default=0, verbose_name="Nº Visitas (Gestante/Puérpera)")
    qtd_consultas_dentista = models.IntegerField(default=0, verbose_name="Nº Consultas Dentista")

    data_vacina_dtpa = models.DateField(blank=True, null=True, verbose_name="Vacina dTpa")
    data_testes_1_semestre = models.DateField(blank=True, null=True, verbose_name="Testes Rápidos (1º Semestre)")
    data_testes_3_semestre = models.DateField(blank=True, null=True, verbose_name="Testes Rápidos (3º Semestre)")

    #crianças
    qtd_consultas_crianca = models.IntegerField(default=0, verbose_name="Nº Consultas (Até 2 anos)")
    qtd_visitas_crianca = models.IntegerField(default=0, verbose_name="Nº Visitas Domiciliares (Até 2 anos)")

    info_vacina_pentavalente = models.CharField(max_length=100, blank=True, null=True, verbose_name="Info Vacina Pentavalente")
    info_vacina_triplice_viral = models.CharField(max_length=100, blank=True, null=True, verbose_name="Info Vacina Tríplice Viral")
    info_vacina_polio = models.CharField(max_length=100, blank=True, null=True, verbose_name="Info Vacina Poliomielite")
    info_vacina_pneumo = models.CharField(max_length=100, blank=True, null=True, verbose_name="Info Vacina Pneumocócica")

    #mulheres
    data_vacina_hpv = models.DateField(blank=True, null=True, verbose_name="Vacina HPV")
    data_consulta_saude_mulher = models.DateField(blank=True, null=True, verbose_name="Consulta Saúde Sexual/Reprodutiva")

    data_exame_citopatologico = models.DateField(blank=True, null=True, verbose_name="Data Exame Citopatológico")
    status_exame_citopatologico = models.CharField(max_length=50, blank=True, null=True, verbose_name="Status Citopatológico (Solicitado/Avaliado)")

    data_mamografia = models.DateField(blank=True, null=True, verbose_name="Mamografia")
    status_mamografia = models.CharField(max_length=50, blank=True, null=True, verbose_name="Status Mamografia (Solicitada/Realizada/Avaliada)")

    #idoso
    data_vacina_influenza = models.DateField(blank=True, null=True, verbose_name="Vacina Influenza (Idoso)")

    def __str__(self):
        return self.nome

    @property
    def idade(self):
        if self.data_nascimento:
            hoje = date.today()
            idade = hoje.year - self.data_nascimento.year - ((hoje.month,hoje.day) < (self.data_nascimento.month, self.data_nascimento.day))
            return idade
        return None

    class Meta:
        verbose_name = "Cidadão"
        verbose_name_plural = "Cidadãos"


    @property
    def status_consulta_diabetico(self):
        if not self.data_consulta_1:
            return "🔴 Vermelho (Sem consulta)"
        dias_passados = (date.today() - self.data_consulta_1).days

        if dias_passados <= 150: 
            return "🟢 Verde"
        elif 150 < dias_passados <= 365: 
            return "🟡 Amarelo"
        else: 
            return "🔴 Vermelho"        
        
    @property
    def status_hemoglobina(self):
        if not self.data_hemoglobina_glicada:
            return "🔴 Vermelho (Sem Hbc1a)"
        
        dias_passados = (date.today() - self.data_hemoglobina_glicada).days

        if dias_passados <=180:
            return "🟢 Verde"
        elif  180 < dias_passados <= 365:
            return  "🟡 Amarelo"
        else:
            return "🔴 Vermelho"
    
    @property
    def classe_cor(self):
        indicadores = []
        grupos_do_cidadao = [grupo.nome for grupo in self.grupos_de_risco.all()]
        
        if "Diabetes" in grupos_do_cidadao:
            indicadores.extend([self.status_consulta_diabetico, self.status_hemoglobina])
            
        if "Hipertensão" in grupos_do_cidadao:
            indicadores.append(self.status_consulta_hipertenso)
            
        if "Gestante" in grupos_do_cidadao:
            indicadores.extend([self.status_pre_natal, self.status_vacina_dtpa, self.status_testes_gestante])

        if not indicadores:
            return "secondary"

        if any("🔴" in status for status in indicadores):
            return "danger"
        elif any("🟡" in status for status in indicadores):
            return "warning"
        
        return "success"

    @property
    def peso_prioridade(self):
        indicadores = []
        grupos_do_cidadao = [grupo.nome for grupo in self.grupos_de_risco.all()]
        
        if "Diabetes" in grupos_do_cidadao:
            indicadores.extend([self.status_consulta_diabetico, self.status_hemoglobina])
        if "Hipertensão" in grupos_do_cidadao:
            indicadores.append(self.status_consulta_hipertenso)
        if "Gestante" in grupos_do_cidadao:
            indicadores.extend([self.status_pre_natal, self.status_vacina_dtpa, self.status_testes_gestante])

        if any("🔴" in status for status in indicadores):
            return 1
        elif any("🟡" in status for status in indicadores):
            return 2
        return 3
    
    @property
    def status_consulta_hipertenso(self):
        if not self.data_consulta_1:
            return "🔴 Vermelho (Sem consulta)"
        
        dias_passados = (date.today() - self.data_consulta_1).days
        
        if dias_passados <= 180:
            return "🟢 Verde"
        elif 180 < dias_passados <= 365:
            return "🟡 Amarelo"
        else:
            return "🔴 Vermelho"
        
    @property
    def status_pre_natal(self):
        if self.qtde_consultas_pre_natal >= 7:
            return "🟢 Verde"
        elif self.qtde_consultas_pre_natal > 0:
            return "🟡 Amarelo"
        else:
            return "🔴 Vermelho (Sem consultas)"

    @property
    def status_vacina_dtpa(self):
        if self.data_vacina_dtpa:
            return "🟢 Verde"
        return "🔴 Vermelho (Pendente)"

    @property
    def status_testes_gestante(self):
        if self.data_testes_1_semestre and self.data_testes_3_semestre:
            return "🟢 Verde"
        elif self.data_testes_1_semestre or self.data_testes_3_semestre:
            return "🟡 Amarelo"
        return "🔴 Vermelho (Pendentes)"
        
    