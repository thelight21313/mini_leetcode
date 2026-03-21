from django.urls import path
from . import consumers

websocket_urlpatterns = [
    path('ws/submissions/<int:submission_id>/', consumers.SubmissionConsumer.as_asgi())
]
