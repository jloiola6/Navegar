from django.test import TestCase

# Create your tests here.

# Path: website/apps/user/tests.py
from django.test import TestCase, Client
from django.urls import reverse

from apps.user.models import User

class ViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123',
        )

    def test_login_view(self):
        response = self.client.get(reverse('user:login'))
        self.assertEqual(response.status_code, 200)

    def test_login_view_post(self):
        response = self.client.post(reverse('user:login'), {
            'username': 'testuser',
            'password': 'testpass123',
        })
        self.assertEqual(response.status_code, 302)

    def test_logout_view(self):
        response = self.client.get(reverse('user:logout'))
        self.assertEqual(response.status_code, 302)

    def test_register_view(self):
        response = self.client.get(reverse('user:signup'))
        self.assertEqual(response.status_code, 200)
    
    def test_register_view_post(self):
        response = self.client.post(reverse('user:signup'), {
            'username': 'testuser2',
            'email': 'testeuser2@gmail.com',
            'password1': 'testpass123',
            'password2': 'testpass123',
        })
        self.assertEqual(response.status_code, 302)
