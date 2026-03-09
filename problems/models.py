from django.contrib.auth import get_user_model
from django.db import models
from autoslug import AutoSlugField
User = get_user_model()


class Tag(models.Model):
    name = models.CharField(max_length=50)
    slug = AutoSlugField(populate_from='name', unique=True)


class Problem(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    slug = AutoSlugField(populate_from='title', unique=True)
    solved_count = models.IntegerField(default=0)

    DIFFICULT_CHOICE = [
        ('easy', 'лёгкий'),
        ('medium', 'средний'),
        ('hard', 'трудный')
    ]

    difficulty = models.CharField(choices=DIFFICULT_CHOICE, max_length=10)
    time_limit_ms = models.IntegerField()
    memory_limit_mb = models.IntegerField()

    tags = models.ManyToManyField(Tag, blank=True)
    is_published = models.BooleanField(default=False)

    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)


class TestCase(models.Model):
    input_data = models.TextField()
    output_data = models.TextField()
    is_published = models.BooleanField(default=False)
    problem = models.ForeignKey(Problem, on_delete=models.CASCADE, related_name='test_cases')
    order = models.PositiveIntegerField(default=0)
