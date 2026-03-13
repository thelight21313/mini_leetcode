import django
from rest_framework.renderers import JSONRenderer
from rest_framework import serializers
from problems.models import Problem, Tag, TestCase
from submissions.models import Submission


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['id', 'name']


class ProblemSerializer(serializers.ModelSerializer):
    tags = TagSerializer(many=True)
    solved_percent = serializers.SerializerMethodField()
    user_status = serializers.SerializerMethodField()

    class Meta:
        model = Problem
        fields = ['id', 'slug', 'title', 'difficulty', 'tags', 'solved_percent', 'user_status']

    def get_solved_percent(self, obj):
        total = Submission.objects.filter(task=obj).count()
        if total == 0:
            return 0
        solved = Submission.objects.filter(task=obj, status='accepted').count()
        return solved/total

    def get_user_status(self, obj):
        request = self.context.get('request')
        if not request or not request.user.is_authenticated:
            return None
        submission = Submission.objects.filter(user=request.user, task=obj).order_by('-push_date').first()
        if not submission:  # ← эта проверка обязательна
            return None
        if submission.status == 'accepted':
            return 'accepted'
        return 'attempted'


class TestCaseSerializer(serializers.ModelSerializer):
    input = serializers.CharField(source='input_data')
    output = serializers.CharField(source='output_data')
    class Meta:
        model = TestCase
        fields = ['input', 'output', 'explanation']


class DetailProblemSerializer(ProblemSerializer):
    examples = TestCaseSerializer(source='test_cases', many=True, read_only=True)
    last_submission_code = serializers.SerializerMethodField()

    def get_last_submission_code(self, obj):
        last_submission = Submission.objects.filter(task=obj).order_by('-push_date').first()
        if last_submission:
            return last_submission.code
        return None

    class Meta(ProblemSerializer.Meta):
        model = Problem
        fields = ProblemSerializer.Meta.fields + ['description', 'examples', 'constraints', 'time_limit_ms', 'memory_limit_mb', 'last_submission_code']