import pytest
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import RefreshToken
from problems.models import Problem

User = get_user_model()


@pytest.fixture
def test_user(db):
    return User.objects.create_user(
        username='test_user',
        password='12345678'
    )


@pytest.fixture
def authenticated_user(test_user):
    client = APIClient()
    refresh = RefreshToken.for_user(test_user)
    client.credentials(HTTP_AUTHORIZATION=f'Bearer {refresh.access_token}')
    return client


@pytest.fixture()
def problem_fixture(db):
    return Problem.objects.create(
        title='123',
        slug='123',
        description='123',
        difficulty='easy',
        time_limit_ms=2000,
        memory_limit_mb=300,
        is_published=True
    )
