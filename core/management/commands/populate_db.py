from django.core.management.base import BaseCommand
from faker import Faker
from core.models.system import Disciplina


class Command(BaseCommand):
    help = 'Populate the database with mock data'

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
