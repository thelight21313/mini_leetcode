import pytest
from problems.models import Problem, TestCase
from submissions.models import Submission
from rest_framework.test import APIClient


@pytest.fixture()
def submission_fixture(test_user, problem_fixture, db):
    return Submission.objects.create(
        user=test_user,
        problem=problem_fixture,
        code='123',
        language='python'
    )


class TestApi:
    def test_get(self, authenticated_user, test_user, submission_fixture):
        client = authenticated_user
        response = client.get(f'/api/submission/{submission_fixture.id}/', format='json')

        assert response.status_code == 200
        assert response.data['status'] is not None

    def test_anonymous(self, submission_fixture, test_user):
        client = APIClient()
        response = client.get(f'/api/submission/{submission_fixture.id}/', format='json')

        assert response.status_code == 401
        

