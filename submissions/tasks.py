from celery import shared_task
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
import requests

from problems.models import TestCase

from submissions.models import Submission


def check_test(code, language, stdin, time_limit_ms, memory_limit_mb):
    try:
        response = requests.post(
            'http://judge0:2358/run',
            json={
                'code': code,
                'language': language,
                'stdin': stdin,
                'time_limit_ms': time_limit_ms,
                'memory_limit_mb': memory_limit_mb,
            },
            timeout=30
        )
        response.raise_for_status()
        return response.json()

    except requests.Timeout:
        return {'stdout': None, 'stderr': None, 'runtime_ms': None, 'memory_mb': None, 'error': 'time_limit'}
    except requests.RequestException:
        return {'stdout': None, 'stderr': None, 'runtime_ms': None, 'memory_mb': None, 'error': 'runtime_error'}


def check_submission(submission_id):
    submission = Submission.objects.select_related('problem').get(id=submission_id)
    problem = submission.problem
    test_cases = TestCase.objects.filter(problem=problem)

    for test_case in test_cases:

        result = check_test(submission.code, submission.language,
                            test_case.input_data, problem.time_limit_ms, problem.memory_limit_mb)

        if result['error']:
            submission.status = result['error']
            submission.save()
            break

        if result['stdout'].strip() != test_case.output_data.strip():
            submission.status = 'wrong_answer'
            submission.save()
            break
    else:
        submission.status = 'accepted'
        submission.runtime_ms = result['runtime_ms']
        submission.memory_mb = result['memory_mb']
        submission.save()