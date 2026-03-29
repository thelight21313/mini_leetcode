from django.contrib.auth import get_user_model
from django.db import models
User = get_user_model()


class Contest(models.Model):
    title = models.CharField(max_length=50)
    description = models.TextField()
    start_date = models.DateTimeField()

    duration_min = models.IntegerField()

    @property
    def status(self):
        from django.utils import timezone
        now = timezone.now()
        if now < self.start_date:
            return 'upcoming'
        if now > self.end_date:
            return 'finished'
        return 'active'

    problems = models.ManyToManyField('problems.Problem', related_name='contest')

    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

    participants = models.ManyToManyField(User, through='ContestParticipant', related_name='contests', blank=True)


class ContestParticipant(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    register_date = models.DateTimeField(auto_now_add=True)
    contest = models.ForeignKey(Contest, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('user', 'contest')
