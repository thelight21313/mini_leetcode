from django.shortcuts import render
from rest_framework import viewsets

from leet_code.problems.models import Problem, Tag


class ProblemViewSet(viewsets.ModelViewSet):
    lookup_field = 'slug'
    queryset = Problem.objects.all()


class TagViewSet(viewsets.ModelViewSet):
    lookup_field = 'slug'
    queryset = Tag.objects.all()
