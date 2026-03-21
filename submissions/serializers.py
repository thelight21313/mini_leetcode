import django
from rest_framework.renderers import JSONRenderer
from rest_framework import serializers

from problems.models import Problem
from submissions.models import Submission


class SubmissionSerializer(serializers.ModelSerializer):
    problem_slug = serializers.SlugRelatedField(
        slug_field='slug',
        queryset=Problem.objects.all(),
        source='problem'
    )

    class Meta:
        model = Submission
        fields = ['id', 'code', 'problem_slug', 'language', 'status', 'runtime_ms', 'memory_mb', 'created_at']
        read_only_fields = ['id', 'status', 'runtime_ms', 'memory_mb', 'created_at']
