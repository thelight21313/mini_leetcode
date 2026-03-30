from datetime import timedelta

from rest_framework import serializers
from .models import Contest


class ContestSerializer(serializers.ModelSerializer):
    start_time = serializers.CharField(source='start_date')
    end_time = serializers.CharField(source='end_date')
    participants_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = Contest
        fields = ['title', 'id', 'status', 'start_time', 'end_time', 'participants_count']


class DetailContestSerializer(serializers.ModelSerializer):
    start_time = serializers.CharField(source='start_date')
    end_time = serializers.SerializerMethodField()
    problems_count = serializers.IntegerField(read_only=True)
    participants_count = serializers.IntegerField(read_only=True)
    is_registered = serializers.BooleanField(read_only=True)
    class Meta:
        model = Contest
        fields = ['title', 'id', 'start_time', 'problems', 'end_time',
                  'problems_count', 'participants_count', 'is_registered']
        
    def get_end_time(self, obj):
        if obj.start_date is not None and obj.duration_min is not None:
            return obj.start_date + timedelta(minutes=obj.duration_min)
        return None