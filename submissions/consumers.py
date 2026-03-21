from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
import json

from rest_framework_simplejwt.tokens import AccessToken

from submissions.models import Submission
from users.models import User


class SubmissionConsumer(AsyncWebsocketConsumer):

    @database_sync_to_async
    def check_access(self):
        try:
            token_key = self.scope['query_string'].decode().split('token=')[-1]
            token = AccessToken(token_key)
            user = User.objects.get(id=token['user_id'])
            self.submission = Submission.objects.get(id = self.submission_id)
            return self.submission.user == user
        except Exception:
            return False

    async def connect(self):
        self.submission_id = self.scope['url_route']['kwargs']['submission_id']
        self.group_name = f'submission_{self.submission_id}'

        has_acces = await self.check_access()
        if not has_acces:
            await self.close()
            return
        await self.channel_layer.group_add(self.group_name, self.channel_name)
        await self.accept()
        result = await self.check_result()
        if result:
            await self.send(text_data=json.dumps(result))
            await self.close()

    @database_sync_to_async
    def check_result(self):
        if self.submission.status not in ['running', 'pending']:
            return {
                'status': self.submission.status,
                'runtime_ms': self.submission.runtime_ms,
                'memory_mb': self.submission.memory_mb,
            }
        return None

    async def disconnect(self, code):
        await self.channel_layer.group_discard(self.group_name, self.channel_name)

    async def submission_update(self, event):
        await self.send(text_data=json.dumps(event['data']))
        if event['data']['status'] not in ['running', 'pending']:
            await self.close()
