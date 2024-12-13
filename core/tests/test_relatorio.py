from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from core.models import Usuario, Aluno, Relatorio, Orientador
from datetime import date
from django.utils import timezone


class RelatorioIntegrationTest(TestCase):
    def setUp(self):
        self.client = APIClient()

        self.user_orientador = Usuario.objects.create_user(
            email='orientador@example.com',
            username='orientador_user',
            password='testpassword',
            nome_completo='Orientador User',
            data_nascimento=date(1980, 5, 15),
            tipo='Orientador'
        )

        self.orientador = Orientador.objects.create(usuario=self.user_orientador)

        self.user_aluno = Usuario.objects.create_user(
            email='aluno@example.com',
            username='aluno_user',
            password='testpassword',
            nome_completo='Aluno User',
            data_nascimento=date(2000, 1, 1),
            tipo='Aluno'
        )
        self.aluno = Aluno.objects.create(usuario=self.user_aluno, orientador=self.orientador)

        self.relatorio = Relatorio.objects.create(
            aluno=self.aluno,
            semestre="2",
            descricao="Some descricao",
            houve_reavaliacao=False,
            data_entrega=timezone.now().date()
        )
        self.client.force_authenticate(user=self.user_aluno)


    def test_update_relatorio_success(self):
        url = reverse('relatorio_view')
        payload = {
            "relatorioId": self.relatorio.id,
            "semestre": "1",
            "descricao": "Alterado no teste",
            "prazoDeposito": "2025-11-30"
        }
        response = self.client.post(url, payload, format='json')

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json()['message'], "Relatório enviado com sucesso.")

        self.relatorio.refresh_from_db()
        self.assertEqual(self.relatorio.semestre, "1")

"""
    def test_submit_relatorio_without_id(self):
        url = reverse('relatorio_view')
        payload = {
            "qualificacao": "No ID qualificacao",
        }
        response = self.client.post(url, payload, format='json')

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()['error'], "ID do relatório não fornecido.")

    def test_non_aluno_cannot_submit_relatorio(self):
        self.client.force_authenticate(user=self.user_orientador)
        url = reverse('relatorio_view')
        payload = {
            "relatorioId": self.relatorio.id,
            "qualificacao": "Invalid user qualificacao",
        }
        response = self.client.post(url, payload, format='json')

        self.assertEqual(response.status_code, 403)
        self.assertEqual(response.json()['error'], "Apenas alunos podem submeter relatórios.")

    def test_unauthenticated_user_cannot_submit_relatorio(self):
        self.client.force_authenticate(user=None)
        url = reverse('relatorio_view')
        payload = {
            "relatorioId": self.relatorio.id,
            "qualificacao": "No auth qualificacao",
        }
        response = self.client.post(url, payload, format='json')

        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.json()['error'], "Usuário não autenticado.")

    def test_update_nonexistent_relatorio(self):
        url = reverse('relatorio_view')
        payload = {
            "relatorioId": 999,
            "qualificacao": "Nonexistent qualificacao",
        }
        response = self.client.post(url, payload, format='json')

        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json()['error'], "Relatório não encontrado ou não pertence ao aluno.")
"""