import django_filters
from django.db.models import Q
from django_filters import BaseCSVFilter

from problems.models import Problem, Tag


class ProblemFilter(django_filters.FilterSet):
    search = django_filters.CharFilter(method='search_filter')
    difficulty = BaseCSVFilter(field_name='difficulty', lookup_expr='in')
    tags = django_filters.CharFilter(method='filter_by_tags')

    class Meta:
        model = Problem
        fields = ['tags', 'difficulty', 'search']

    def search_filter(self, queryset, name, value):
        return queryset.filter(
            Q(title__icontains=value) |
            Q(description__icontains=value) |
            Q(tags__name__icontains=value)
        )

    def filter_by_tags(self, queryset, name, value):
        tag_list = value.split(',')
        for tag in tag_list:
            queryset = queryset.filter(tags__name=tag)
        return queryset.distinct()