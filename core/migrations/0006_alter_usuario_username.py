# Generated by Django 4.2.16 on 2024-12-08 14:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0005_alter_usuario_managers_usuario_date_joined_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usuario',
            name='username',
            field=models.CharField(blank=True, max_length=150, null=True),
        ),
    ]
