import pytest
from problems.models import Problem, TestCase
from submissions.models import Submission


@pytest.fixture()
def test_case_fixture(problem_fixture, db):
    return TestCase.objects.create(
        input_data='123',
        output_data='123',
        problem=problem_fixture,
        explanation='no'
    )


class TestStatus:
    @pytest.fixture(autouse=True)
    def setup(self, authenticated_user, problem_fixture):
        self.client = authenticated_user
        self.problem = problem_fixture

    def test_accept(self, test_case_fixture):
        response = self.client.post('/api/submission/', data={
            'problem_slug': self.problem.slug,
            'code': 'print(123)',
            'language': 'python'
        }, format='json')

        submission = Submission.objects.get(problem__slug=self.problem.slug)

        assert response.status_code == 201
        assert submission.status == 'accepted'
        assert submission.runtime_ms is not None
        assert submission.memory_mb is not None

    def test_wrong(self, test_case_fixture):
        response = self.client.post('/api/submission/', data={
            'problem_slug': self.problem.slug,
            'code': 'print("wrong")',
            'language': 'python'
        }, format='json')

        submission = Submission.objects.get(problem__slug=self.problem.slug)

        assert response.status_code == 201
        assert submission.status == 'wrong_answer'
        assert submission.runtime_ms is None
        assert submission.memory_mb is None

    def test_runtime(self, test_case_fixture):
        response = self.client.post('/api/submission/', data={
            'problem_slug': self.problem.slug,
            'code': 'asdf',
            'language': 'python'
        }, format='json')
        submission = Submission.objects.get(problem__slug=self.problem.slug)

        assert response.status_code == 201
        assert submission.status == 'runtime_error'
        assert submission.runtime_ms is None
        assert submission.memory_mb is None

    def test_without_testcases(self):
        response = self.client.post('/api/submission/', data={
            'problem_slug': self.problem.slug,
            'code': 'print(123)',
            'language': 'python'
        }, format='json')

        submission = Submission.objects.get(problem__slug=self.problem.slug)

        assert response.status_code == 201
        assert submission.status == 'wrong_answer'
        assert submission.runtime_ms is None
        assert submission.memory_mb is None

