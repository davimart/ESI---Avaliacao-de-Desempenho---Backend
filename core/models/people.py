from django.db import models


class Usuario(models.Model):
    id = models.AutoField(primary_key=True)
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

    class Meta:
        db_table = 'Usuario'


class Aluno(models.Model):
    id_matricula = models.CharField(max_length=50, unique=True)
    usuario = models.OneToOneField(Usuario, on_delete=models.CASCADE, primary_key=True)
    orientador = models.ForeignKey('Orientador', on_delete=models.CASCADE)
    disciplinas = models.ManyToManyField('core.Disciplina', related_name="alunos")

    class Meta:
        db_table = 'Aluno'


class Orientador(models.Model):
    usuario = models.OneToOneField(Usuario, on_delete=models.CASCADE, primary_key=True)
    numero_alunos_orientados = models.IntegerField(default=0)

    class Meta:
        db_table = 'Orientador'
