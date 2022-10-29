from django.db import models
from django.contrib.auth.models import User

# Create your models here.



class Todo(models.Model):
    title = models.CharField(max_length=100)
    memo = models.TextField(blank=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    datecompleted = models.DateTimeField(null=True, blank=True)
    important = models.BooleanField(default=False)
    status = models.BooleanField(default=False)

    def __str__(self):
        return self.title