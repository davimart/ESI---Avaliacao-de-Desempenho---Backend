from django.db import models
from django.contrib.auth.models import AbstractUser

class Usuario(AbstractUser):
    id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=150, blank=True, null=True)
    nome_completo = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    data_nascimento = models.DateField()
    rg = models.CharField(max_length=50, blank=True, null=True)
    local_nascimento = models.CharField(max_length=100, blank=True, null=True)
    nacionalidade = models.CharField(max_length=50, blank=True, null=True)
    curso = models.CharField(max_length=50)
    link_lattes = models.URLField(blank=True, null=True)
    data_matricula = models.DateField(blank=True, null=True)
    data_aprovacao_exame_qualificacao = models.DateField(blank=True, null=True)
    data_aprovacao_exame_proficiencia = models.DateField(blank=True, null=True)
    data_limite_deposito_trabalho = models.DateField(blank=True, null=True)
    tipo = models.CharField(max_length=50, choices=[
        ('Aluno', 'Aluno'),
        ('Orientador', 'Orientador'),
        ('Comissao', 'Comissao')
    ])

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['nome_completo', 'tipo']

    groups = models.ManyToManyField(
        'auth.Group',
        related_name='usuario_set',
        blank=True
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='usuario_set',
        blank=True
    )

    class Meta:
        db_table = 'Usuario'

class Disciplina(models.Model):
    nome = models.CharField(max_length=255)
    professor = models.CharField(max_length=255)
    numero_alunos = models.IntegerField()
    periodo = models.CharField(max_length=50, choices=[
        ('Noturno', 'Noturno'),
        ('Diurno', 'Diurno'),
        ('Matutino', 'Matutino'),
        ('Integral', 'Integral')
    ])
    semestre = models.CharField(max_length=50)
    sala = models.CharField(max_length=50)

    class Meta:
        db_table = 'Disciplina'

class Aluno(models.Model):
    id_matricula = models.CharField(max_length=50, unique=True)
    usuario = models.OneToOneField(Usuario, on_delete=models.CASCADE, primary_key=True)
    orientador = models.ForeignKey('Orientador', on_delete=models.CASCADE)
    disciplinas = models.ManyToManyField(Disciplina, related_name="alunos")
    class Meta:
        db_table = 'Aluno'

class Orientador(models.Model):
    usuario = models.OneToOneField(Usuario, on_delete=models.CASCADE, primary_key=True)
    numero_alunos_orientados = models.IntegerField(default=0)

    class Meta:
        db_table = 'Orientador'

class Comissao(models.Model):
    usuario = models.OneToOneField(Usuario, on_delete=models.CASCADE, primary_key=True)

    class Meta:
        db_table = 'Comissao'

class HistoricoDisciplina(models.Model):
    aluno = models.ForeignKey(Aluno, on_delete=models.CASCADE)
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
