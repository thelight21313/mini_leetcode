from datetime import timedelta

from celery import shared_task
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
import requests
from contests.models import Contest, ContestParticipant


@shared_task()
def start_contest(contest_id):
    contest = Contest.objects.get(id=contest_id)
    contest.status = 'active'
    contest.save()

    end_time = contest.start_date + timedelta(minutes=contest.duration_min)

    finish_contest.apply_async(args=[contest_id], eta=end_time)


@shared_task()
def finish_contest(contest_id):
    contest = Contest.object.get(id=contest_id)
    contest.status = 'finished'
    contest.save()
