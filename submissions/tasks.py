from celery import shared_task
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
import requests

from problems.models import TestCase

from submissions.models import Submission


def notify_submission(submission):
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        f'submission_{submission.id}',
        {
            'type': 'submission_update',
            'data': {
                'status': submission.status,
                'runtime_ms': submission.runtime_ms,
                'memory_mb': submission.memory_mb
            }
        }
    )


def _get_language_id(language):
    return {
        'python': 71,
        'javascript': 63,
        'go': 60,
        'cpp': 54,
    }.get(language, 71)


def status(stat):
    return {
        3: None,
        4: 'wrong_answer',
        5: 'time_limit',
        6: 'compilation_error',
        7: 'runtime_error', 8: 'runtime_error',
        9: 'runtime_error', 10: 'runtime_error',
        11: 'runtime_error', 12: 'runtime_error',
        14: 'memory_limit',
    }.get(stat, 'runtime_error')


def check_test(code, language, stdin, time_limit_ms, memory_limit_mb):
    try:
        response = requests.post(
            'http://judge0:2358/submissions?wait=true',
            json={
                'source_code': code,
                'language_id': _get_language_id(language),
                'stdin': stdin,
                'cpu_time_limit': time_limit_ms / 1000,
                'memory_limit': memory_limit_mb * 1024,
            },
            timeout=30
        )
        result = response.json()
        return {
            'stdout': result.get('stdout'),
            'stderr': result.get('stderr'),
            'runtime_ms': int(float(result.get('time') or 0) * 1000),
            'memory_mb': int((result.get('memory') or 0) / 1024),
            'error': status(result.get('status', {}).get('id'))

        }

    except requests.Timeout:
        return {'stdout': None, 'stderr': None, 'runtime_ms': None, 'memory_mb': None, 'error': 'time_limit'}
    except requests.RequestException:
        return {'stdout': None, 'stderr': None, 'runtime_ms': None, 'memory_mb': None, 'error': 'runtime_error'}


@shared_task
def check_submission(submission_id):
    submission = Submission.objects.select_related('problem').get(id=submission_id)
    problem = submission.problem
    test_cases = TestCase.objects.filter(problem=problem)
    submission.status = 'running'
    submission.save()
    notify_submission(submission)

    for test_case in test_cases:

        result = check_test(submission.code, submission.language,
                            test_case.input_data, problem.time_limit_ms, problem.memory_limit_mb)

        if result['error']:
            submission.status = result['error']
            submission.save()
            notify_submission(submission)
            break

        stdout = (result['stdout'] or '').strip()
        if stdout != test_case.output_data.strip():
            submission.status = 'wrong_answer'
            submission.save()
            notify_submission(submission)
            break
    else:
        submission.status = 'accepted'
        submission.runtime_ms = result['runtime_ms']
        submission.memory_mb = result['memory_mb']
        submission.save()
        notify_submission(submission)
