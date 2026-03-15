from celery import shared_task
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

from submissions.models import Submission


def check_submission(submission_id):
    pass
