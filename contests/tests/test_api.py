from datetime import timedelta
from rest_framework.test import APIClient
import pytest
from contests.models import Contest, ContestParticipant
from submissions.models import Submission
from django.utils import timezone


@pytest.fixture()
def contest_fixture(db, problem_fixture):
    now = timezone.now()
    contest = Contest.objects.create(
        title='contest',
        description='test',
        start_date=now-timedelta(minutes=10),
        duration_min=60,
    )
    contest.problems.add(problem_fixture)

    return contest


class TestRegister:
    def test_register(self, contest_fixture, authenticated_user, db, test_user):
        client = authenticated_user
        response = client.post(f'/api/contests/{contest_fixture.id}/register/', format='json')

        assert response.status_code == 200
        assert ContestParticipant.objects.filter(user=test_user).exists()

    def test_double_registration(self, contest_fixture, authenticated_user, db, test_user):
        client = authenticated_user
        response1 = client.post(f'/api/contests/{contest_fixture.id}/register/', format='json')
        response2 = client.post(f'/api/contests/{contest_fixture.id}/register/', format='json')

        contest = ContestParticipant.objects.filter(user=test_user)

        assert response2.status_code == 400
        assert contest.exists()
        assert contest.count() == 1


class TestSubmit:
    def test_submit_without_register(self, contest_fixture, authenticated_user, problem_fixture):
        client = authenticated_user
        response = client.post(f'/api/contests/{contest_fixture.id}/submit/', data={
            'problem_slug': problem_fixture.slug,
            'code': 'print(123)',
            'language': 'python'
        }, format='json')

        assert response.status_code == 403

    def test_submit_after_end(self, problem_fixture, authenticated_user):
        now = timezone.now()
        contest = Contest.objects.create(
            title='contest',
            description='test',
            start_date=now - timedelta(minutes=70),
            duration_min=60,
        )
        contest.problems.add(problem_fixture)

        client = authenticated_user
        response1 = client.post(f'/api/contests/{contest.id}/register/', format='json')
        response = client.post(f'/api/contests/{contest.id}/submit/', data={
            'problem_slug': problem_fixture.slug,
            'code': 'print(123)',
            'language': 'python'
        }, format='json')

        assert response.status_code == 400

    def test_problem_not_from_contest(self, authenticated_user, contest_fixture):
        client = authenticated_user
        response = client.post(f'/api/contests/{contest_fixture.id}/submit/', data={
            'problem_slug': 'not exists',
            'code': 'print(123)',
            'language': 'python'
        }, format='json')

        assert response.status_code == 400


class TestProblemList:
    def test_list_without_register(self, contest_fixture, authenticated_user):
        client = authenticated_user
        response = client.get(f'/api/contests/{contest_fixture.id}/problems/')

        assert response.status_code == 403

    def test_list_with_register(self, contest_fixture, authenticated_user):
        client = authenticated_user
        response1 = client.post(f'/api/contests/{contest_fixture.id}/register/', format='json')
        response = client.get(f'/api/contests/{contest_fixture.id}/problems/')

        assert response.status_code == 200
