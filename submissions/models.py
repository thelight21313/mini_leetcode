from django.contrib.auth import get_user_model
from django.db import models
User = get_user_model()


class Submission(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    problem = models.ForeignKey('problems.Problem', on_delete=models.CASCADE, related_name='submissions')
    contest = models.ForeignKey('contests.Contest', on_delete=models.SET_NULL, null=True, blank=True)
    code = models.TextField()

    LANGUAGE_CHOICE = [
        ('python', 'Python')
    ]
    STATUS_CHOICE = [
        ('pending', 'ожидание'),
        ('running', 'запущен'),
        ('accepted', 'принят'),
        ('wrong_answer', 'неправильный ответ'),
        ('time_limit', 'превышен лимит времени'),
        ('memory_limit', 'превышен лимит памяти'),
        ('runtime_error', 'ошибка времени выполнения'),
        ('compilation_error', 'ошибка компиляции')
    ]

    language = models.CharField(choices=LANGUAGE_CHOICE, max_length=20)
    status = models.CharField(choices=STATUS_CHOICE, max_length=50, default='pending')

    runtime_ms = models.IntegerField(null=True)
    memory_mb = models.IntegerField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)
