from django.test import TestCase, Client
from django.urls import reverse
from core.models import Usuario
from datetime import date


class LoginIntegrationTest(TestCase):
    def setUp(self):
        self.user = Usuario.objects.create_user(
            email='testuser@example.com',
            username='testuser',
            password='testpassword123',
            nome_completo='Test User',
            tipo='Aluno',
            data_nascimento=date(2000, 1, 1)
        )
        self.client = Client()
        self.login_url = reverse('login')

    def test_login_success(self):
        login_data = {
            'email': 'testuser@example.com',
            'password': 'testpassword123'
        }

        response = self.client.post(self.login_url, login_data)

        self.assertEqual(response.status_code, 200)

        self.assertIn('token', response.json())
        self.assertEqual(response.json()['nome_completo'], 'Test User')


    def test_login_failure_invalid_password(self):
        login_data = {
            'email': 'testuser@example.com',
            'password': 'wrongpassword'
        }

        response = self.client.post(self.login_url, login_data)

        self.assertEqual(response.status_code, 400)

        self.assertIn('error', response.json())
        self.assertEqual(response.json()['error'], 'Invalid credentials')


    def test_login_failure_nonexistent_user(self):
        login_data = {
            'email': 'nonexistent@example.com',
            'password': 'testpassword123'
        }

        response = self.client.post(self.login_url, login_data)

        self.assertEqual(response.status_code, 400)

        self.assertIn('error', response.json())
        self.assertEqual(response.json()['error'], 'Invalid credentials')
