from django.db import models
from django.urls import reverse


class Job(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return f'{self.name}'


class Person(models.Model):
    job = models.ForeignKey(Job, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    is_active = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.first_name} {self.last_name}'
