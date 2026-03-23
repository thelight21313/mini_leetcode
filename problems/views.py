from django.db.models import Count, Q, Subquery, OuterRef
from django.shortcuts import render
from rest_framework import viewsets

from problems.models import Problem, Tag
from problems.serializers import TagSerializer, ProblemSerializer, DetailProblemSerializer
from rest_framework.decorators import action
from rest_framework.response import Response

from submissions.models import Submission


class ProblemViewSet(viewsets.ModelViewSet):
    serializer_class = ProblemSerializer
    lookup_field = 'slug'

    def get_queryset(self):
        qs = Problem.objects.all().order_by('id').prefetch_related('tags').annotate(
            total=Count('submissions'),
            accepted=Count('submissions', filter=Q(submissions__status='accepted'))
        )
        if self.request.user.is_authenticated:
            qs = qs.annotate(
                last_status=Subquery(
                    Submission.objects.filter(
                        user=self.request.user,
                        problem=OuterRef('pk')
                    ).order_by('-created_at').values('status')[:1])
            )
        return qs

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return DetailProblemSerializer
        return super().get_serializer_class()

    @action(detail=True, methods=['get'])
    def detail_problem(self, request, slug=None):
        problem = self.get_object()
        serializer = self.get_serializer(problem)
        return Response(serializer.data)



class TagViewSet(viewsets.ModelViewSet):
    lookup_field = 'slug'
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
