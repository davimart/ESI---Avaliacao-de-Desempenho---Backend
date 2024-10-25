from django.db import models

from core.models.people import Usuario, Aluno, Orientador


class Comissao(models.Model):
    usuario = models.OneToOneField(Usuario, on_delete=models.CASCADE, primary_key=True)
    
    class Meta:
        db_table = 'Comissao'


class Disciplina(models.Model):
    nome = models.CharField(max_length=255)
    professor = models.CharField(max_length=255)
    numero_alunos = models.IntegerField()
    periodo = models.CharField(max_length=50)
    semestre = models.CharField(max_length=50)
    sala = models.CharField(max_length=50)
    
    class Meta:
        db_table = 'Disciplina'


class RelatorioDesempenho(models.Model):
    aluno = models.ForeignKey(Aluno, on_delete=models.CASCADE)
    orientador = models.ForeignKey(Orientador, on_delete=models.CASCADE)
    comissao = models.ForeignKey(Comissao, on_delete=models.SET_NULL, blank=True, null=True)
    data_limite = models.DateField()
    status = models.CharField(max_length=50)  # 'Aberto', 'Avaliando', 'Fechado'
    conceito_orientador = models.CharField(max_length=50, blank=True, null=True)  # 'Adequado', 'Adequado com Ressalvas', 'Insatisfatorio'
    conceito_comissao = models.CharField(max_length=50, blank=True, null=True)  # 'Adequado', 'Adequado com Ressalvas', 'Insatisfatorio'
    houve_reavaliacao = models.BooleanField(default=False)

    class Meta:
        db_table = 'RelatorioDesempenho'


class HistoricoDisciplina(models.Model):
    aluno = models.ForeignKey(Aluno, on_delete=models.CASCADE)
    disciplina = models.ForeignKey(Disciplina, on_delete=models.CASCADE)
    status = models.CharField(max_length=50)  # 'Aprovado', 'Reprovado'
    
    class Meta:
        db_table = 'HistoricoDisciplina'


class Relatorio(models.Model):
    aluno = models.ForeignKey(Aluno, on_delete=models.CASCADE)
    data_entrega = models.DateField(null=True, blank=True)
    semestre = models.CharField(max_length=50)
    descricao = models.TextField()
    houve_reavaliacao = models.BooleanField(default=False)

    class Meta:
        db_table = 'Relatorio'


class Avaliacao(models.Model):
    relatorio = models.ForeignKey(Relatorio, on_delete=models.CASCADE)
    avaliador = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    parecer = models.TextField()
    conceito = models.CharField(max_length=50, choices=[
        ('Adequado', 'Adequado'),
        ('Adequado com Ressalvas', 'Adequado com Ressalvas'),
        ('Insatisfatório', 'Insatisfatório')
    ])
    data_avaliacao = models.DateField()

    class Meta:
        db_table = 'Avaliacao'


class Chamado(models.Model):
    relatorio = models.ForeignKey(Relatorio, on_delete=models.CASCADE)
    status = models.CharField(max_length=50, choices=[
        ('Aberto', 'Aberto'),
        ('Avaliando', 'Avaliando'),
        ('Fechado', 'Fechado')
    ])
    data_abertura = models.DateField()
    data_fechamento = models.DateField(null=True, blank=True)

    class Meta:
        db_table = 'Chamado'
