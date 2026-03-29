import redis

from submissions.models import Submission


@staticmethod
def update_leaderboard(user_id, contest_id):
    r = redis.Redis(host='redis', port=6379, db=0)
    solved_count = Submission.objects.filter(contest_id=contest_id,
                                             user=user_id,
                                             status='accepted').values('problem_id').distinct().count()

    r.zadd(f'leaderboard:contest_id:{contest_id}', {str(user_id): solved_count})
