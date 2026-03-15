from django.shortcuts import render
from rest_framework import viewsets, mixins
from rest_framework.permissions import IsAuthenticated
from submissions.tasks import check_submission
from submissions.models import Submission
from submissions.serializers import SubmissionSerializer


class SubmissionViewSet(mixins.CreateModelMixin,
                        mixins.RetrieveModelMixin,
                        viewsets.GenericViewSet):

    serializer_class = SubmissionSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Submission.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        submission = serializer.save(user=self.request.user)
        check_submission.delay(submission.id)

