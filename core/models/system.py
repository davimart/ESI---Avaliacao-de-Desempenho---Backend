from django.db import models

from core.models.people import Usuario, Aluno


class Disciplina(models.Model):
    nome = models.CharField(max_length=255)
    professor = models.CharField(max_length=255)
    numero_alunos = models.IntegerField()
    periodo = models.CharField(max_length=50)
    semestre = models.CharField(max_length=50)
    sala = models.CharField(max_length=50)

    class Meta:
        db_table = 'Disciplina'


class Comissao(models.Model):
    usuario = models.OneToOneField('core.Usuario', on_delete=models.CASCADE, primary_key=True)

    class Meta:
        db_table = 'Comissao'


class HistoricoDisciplina(models.Model):
    aluno = models.ForeignKey('core.Aluno', on_delete=models.CASCADE)
    disciplina = models.ForeignKey(Disciplina, on_delete=models.CASCADE)
    status = models.CharField(max_length=50, choices=[
        ('Aprovado', 'Aprovado'),
        ('Reprovado', 'Reprovado')
    ])

    class Meta:
        db_table = 'HistoricoDisciplina'


class Avaliacao(models.Model):
    avaliador = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    parecer = models.TextField()
    conceito = models.CharField(max_length=50, choices=[
        ('Adequado', 'Adequado'),
        ('Adequado com Ressalvas', 'Adequado com Ressalvas'),
        ('Insatisfatório', 'Insatisfatório')
    ])
    status = models.CharField(max_length=50, choices=[
        ('Aberto', 'Aberto'),
        ('Avaliando', 'Avaliando'),
        ('Fechado', 'Fechado')
    ])
    data_avaliacao = models.DateField()

    class Meta:
        db_table = 'Avaliacao'


class Relatorio(models.Model):
    aluno = models.ForeignKey(Aluno, on_delete=models.CASCADE)
    data_entrega = models.DateField(null=True, blank=True)
    semestre = models.CharField(max_length=50)
    descricao = models.TextField()
    houve_reavaliacao = models.BooleanField(default=False)
    desempenho = models.ForeignKey(Avaliacao, on_delete=models.CASCADE, null=True, blank=True)

    class Meta:
        db_table = 'Relatorio'


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
