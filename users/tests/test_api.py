import pytest
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient


class TestAccount:
    def test_register(self, db):
        User = get_user_model()
        client = APIClient()
        response = client.post('/api/auth/registration/', data={
            "username": "enix",
            "email": "123@asd.com",
            "password1": "geoguesser",
            "password2": "geoguesser"
        }, format='json')

        assert User.objects.filter(username='enix').exists()
        assert response.status_code == 201

    def test_login_return_tokens(self, db):
        client = APIClient()
        response1 = client.post('/api/auth/registration/', data={
            "username": "enix",
            "email": "123@asd.com",
            "password1": "geoguesser",
            "password2": "geoguesser"
        }, format='json')

        response = client.post('/api/token/', data={
            'username': 'enix',
            'password': 'geoguesser'
        }, format='json')

        assert response.status_code == 200
        assert 'access' in response.data
        assert 'refresh' in response.data
        assert len(response.data['access']) > 0
        assert len(response.data['refresh']) > 0

    def test_wrong_password_login(self,db):
        client = APIClient()
        response1 = client.post('/api/auth/registration/', data={
            "username": "enix",
            "email": "123@asd.com",
            "password1": "geoguesser",
            "password2": "geoguesser"
        }, format='json')

        response = client.post('/api/token/', data={
            'username': 'enix',
            'password': 'wrong'
        }, format='json')

        assert response.status_code == 401

