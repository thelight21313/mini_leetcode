from django.contrib.auth import get_user_model
from django.db import models
User = get_user_model()


class Contest(models.Model):
    title = models.CharField(max_length=50)
    description = models.TextField()
    start_date = models.DateTimeField()

    duration_min = models.IntegerField()

    STATUS_CHOICE = [
        ('upcoming', 'предстоит'),
        ('active', 'сейчас идёт'),
        ('finished', 'завершён')
    ]

    status = models.CharField(choices=STATUS_CHOICE)

    problems = models.ManyToManyField('problems.Problem')

    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)


class ContestParticipant(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    contest = models.ForeignKey(Contest, on_delete=models.CASCADE)
    register_date = models.DateTimeField()
    rating_place = models.IntegerField(null=True, blank=True)
