import pytest
from problems.models import Problem, TestCase, Tag


@pytest.fixture()
def tag_fixture(db):
    return Tag.objects.create(name='test')


@pytest.fixture()
def problem_fixture2(db, tag_fixture):
    problem = Problem.objects.create(
        title='yono',
        description='123',
        difficulty='easy',
        time_limit_ms=2000,
        memory_limit_mb=300,
        is_published=True,
    )
    problem.tags.add(tag_fixture)
    return problem

@pytest.fixture()
def problem_fixture3(db):
    problem = Problem.objects.create(
        title='yono',
        description='123',
        difficulty='easy',
        time_limit_ms=2000,
        memory_limit_mb=300,
        is_published=False,
    )
    return problem


class TestApi:
    def test_difficulty_filter(self, problem_fixture, authenticated_user, problem_fixture2):
        client = authenticated_user
        response = client.get('/api/problems/?difficulty=easy')

        assert len(response.data['results']) == 2

        response1 = client.get('/api/problems/?difficulty=medium')

        assert len(response1.data['results']) == 0

    def test_tags_filter(self, problem_fixture, problem_fixture2, authenticated_user):
        client = authenticated_user
        response = client.get('/api/problems/?tags=test')

        assert len(response.data['results']) == 1

    def test_detail_not_public(self, problem_fixture3, authenticated_user):
        client = authenticated_user
        response = client.get(f'/api/problems/{problem_fixture3.slug}/')

        assert response.status_code == 404
