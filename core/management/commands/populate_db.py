from django.core.management.base import BaseCommand
from django.db import IntegrityError
from faker import Faker
from core.models import Aluno, Usuario, Orientador, Comissao, Disciplina, Relatorio, Avaliacao, Chamado
from datetime import date, timedelta
import random


class Command(BaseCommand):
    help = 'Populate the database with mock data'

    '''
    def handle(self, *args, **kwargs):
        fake = Faker()

        for _ in range(5):
            Disciplina.objects.create(
                nome=fake.word(),
                professor=fake.name(),
                numero_alunos=fake.random_int(min=5, max=30),
                periodo=fake.random_element(elements=('1', '2', '3')),
                semestre=fake.random_element(elements=('2023.1', '2023.2')),
                sala=fake.random_element(elements=('101', '102', '103')),
            )
        self.stdout.write(self.style.SUCCESS('Successfully populated the database with mock data.'))
    '''
    
    def handle(self, *args, **kwargs):
        fake = Faker()
        try:
            orientador_usuario = Usuario.objects.create(
                nome_completo=fake.name(),
                email=fake.email(),
                data_nascimento=fake.date_of_birth(minimum_age=30, maximum_age=60),
                curso="Mestrado",
                tipo="Orientador"
            )
            orientador = Orientador.objects.create(usuario=orientador_usuario)

            aluno_usuario = Usuario.objects.create(
                nome_completo=fake.name(),
                email=fake.unique.email(),
                data_nascimento=fake.date_of_birth(minimum_age=18, maximum_age=28),
                curso="Mestrado",
                tipo="Aluno"
            )

            disciplina = Disciplina.objects.create(
                nome=fake.word().capitalize(),
                professor=fake.name(),
                numero_alunos=random.randint(10, 30),
                periodo=random.choice(["Matutino", "Vespertino", "Noturno"]),
                semestre=random.choice(["2023.1", "2023.2", "2024.1", "2024.2"]),
                sala=f"{random.choice(['A', 'B', 'C'])}{random.randint(1, 10)}"
            )

            aluno = Aluno.objects.create(
                id_matricula=fake.unique.random_number(digits=8),
                usuario=aluno_usuario,
                orientador=orientador
            )
            aluno.disciplinas.add(disciplina)

            orientador.numero_alunos_orientados += 1
            orientador.save()

            self.stdout.write(self.style.SUCCESS("Database populated successfully with mock data."))
        except IntegrityError as e:
            self.stdout.write(self.style.WARNING(f"Data already exists. Skipping insertion: {e}"))


                

