import datetime

import redis
from django.db.models import Count, Q, Subquery, OuterRef, Exists, Value
from django.shortcuts import render
from django.utils import timezone
from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from submissions.serializers import SubmissionSerializer
from rest_framework.decorators import action
from rest_framework.response import Response
from contests.models import Contest, ContestParticipant
from submissions.models import Submission
from submissions.tasks import check_submission
from contests.serializer import ContestSerializer, DetailContestSerializer
from problems.serializers import ProblemSerializer


class ContestViewSet(viewsets.ModelViewSet):
    def get_queryset(self):
        user = self.request.user
        return Contest.objects.prefetch_related('participants',
                                                    'author',
                                                    'problems').order_by('-start_date').annotate(
            problems_count=Count('problems', distinct=True),
            participants_count=Count('participants', distinct=True),
            is_registered=Exists(ContestParticipant.objects.filter(
                user=user,
                contest=OuterRef('pk')) if user.is_authenticated else Value(False)
            )
        )
    permission_classes = [IsAuthenticated]
    serializer_class = ContestSerializer

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return DetailContestSerializer
        if self.action == 'problems':
            return ProblemSerializer
        return super().get_serializer_class()

    def get_permissions(self):
        if self.action in ['create', 'update', 'destroy', 'partial_update']:
            return [IsAdminUser()]
        return [IsAuthenticated()]

    @action(methods=['post'], detail=True)
    def submit(self, request, pk=None):
        user = request.user
        contest = self.get_object()
        serializer = SubmissionSerializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        submission = serializer.save(user=user, contest=contest)

        check_submission.delay(submission.id)
        return Response(SubmissionSerializer(submission).data, status=201)

    @action(methods=['get'], detail=True)
    def problems(self, request, pk=None):
        contest = self.get_object()
        if contest.start_date < timezone.now() and contest.participants.filter(id=request.user.id).exists():
            problems = contest.problems.all()
            serializer = self.get_serializer(problems, many=True)
            return Response(serializer.data)
        else:
            return Response(status=status.HTTP_403_FORBIDDEN)

    @action(methods=['get'], detail=True)
    def leaderboard(self, request, pk=None):
        r = redis.Redis(host='redis', port=6379, db=0)
        r_data = r.zrevrange(f'leaderboard:contest_id:{pk}', 0, 99, withscores=True)
        data = [{
            'user': user_id,
            'score': int(score)
        } for user_id, score in r_data]

        return Response(data)

    @action(methods=['post'], detail=True)
    def register(self, request, pk=None):
        user = request.user
        contest = self.get_object()
        if contest.participants.filter(id=request.user.id).exists():
            return Response(status=status.HTTP_400_BAD_REQUEST)
        else:
            partip = ContestParticipant.objects.create(user=user, contest=contest)
            return Response(status=status.HTTP_200_OK)
