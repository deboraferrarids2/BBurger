# tests.py
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from .models import BaseUser

class CreateUserTests(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_create_user(self):
        url = reverse('user')
        data = {
            'email': 'test@example.com',
            'name': 'John',
            'cpf': '44538646806',
            'password': 'testpassword',
        }

        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(BaseUser.objects.count(), 1)

        user = BaseUser.objects.get()
        self.assertEqual(user.email, data['email'])
        self.assertEqual(user.name, data['name'])
        self.assertEqual(user.cpf.cpf, data['cpf'])

    def test_create_user_missing_field(self):
        url = reverse('user')
        data = {
            'email': 'test@example.com',
            'name': 'John',
            'cpf': '44538646806',  
            #'password': 'testpassword', # Missing password
        }

        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(BaseUser.objects.count(), 0)  # User should not be created

    def test_create_user_invalid_email(self):
        url = reverse('user')
        data = {
            'email': 'invalidemail',  # Invalid email format
            'name': 'John',
            'cpf': '44538646806',
            'password': 'testpassword',
        }

        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(BaseUser.objects.count(), 0)  # User should not be created
