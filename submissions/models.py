from django.contrib.auth import get_user_model
from django.db import models
User = get_user_model()


class Submission(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    task = models.ForeignKey('problems.Problem', on_delete=models.CASCADE)
    contest = models.ForeignKey('contests.Contest', on_delete=models.CASCADE, null=True)
    code = models.TextField()

    LANGUAGE_CHOICE = [
        ('python', 'Python')
    ]
    STATUS_CHOICE = [
        ('pending', 'ожидание'),
        ('running', 'запущен'),
        ('accepted', 'принят'),
        ('wrong answer', 'неправильный ответ'),
        ('time limit', 'превышен лимит времени'),
        ('memory limit', 'превышен лимит памяти'),
        ('runtime error', 'ошибка времени выполнения'),
        ('compilation error', 'ошибка компиляции')
    ]

    language = models.CharField(choices=LANGUAGE_CHOICE, max_length=20)
    status = models.CharField(choices=STATUS_CHOICE, max_length=50, default='pending')

    runtime_ms = models.IntegerField(null=True)
    memory_mb = models.IntegerField(null=True)
    push_date = models.DateTimeField(auto_now_add=True)
