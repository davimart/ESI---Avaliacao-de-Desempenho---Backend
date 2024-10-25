# Generated by Django 4.2.14 on 2024-10-25 18:05

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_aluno_disciplinas'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='avaliacao',
            name='relatorio',
        ),
        migrations.AddField(
            model_name='avaliacao',
            name='status',
            field=models.CharField(choices=[('Aberto', 'Aberto'), ('Avaliando', 'Avaliando'), ('Fechado', 'Fechado')], default=django.utils.timezone.now, max_length=50),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='relatorio',
            name='desempenho',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='core.avaliacao'),
        ),
        migrations.AlterField(
            model_name='historicodisciplina',
            name='status',
            field=models.CharField(choices=[('Aprovado', 'Aprovado'), ('Reprovado', 'Reprovado')], max_length=50),
        ),
        migrations.AlterField(
            model_name='usuario',
            name='tipo',
            field=models.CharField(choices=[('Aluno', 'Aluno'), ('Orientador', 'Orientador'), ('Comissao', 'Comissao')], max_length=50),
        ),
        migrations.DeleteModel(
            name='RelatorioDesempenho',
        ),
    ]