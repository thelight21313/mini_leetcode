from django.shortcuts import render
from rest_framework import viewsets

from problems.models import Problem, Tag
from problems.serializers import TagSerializer, ProblemSerializer, DetailProblemSerializer
from rest_framework.decorators import action
from rest_framework.response import Response


class ProblemViewSet(viewsets.ModelViewSet):
    queryset = Problem.objects.all().order_by('id')
    serializer_class = ProblemSerializer
    lookup_field = 'slug'

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
