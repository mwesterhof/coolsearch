from django.db import models
from django.urls import reverse


class Job(models.Model):
    name = models.CharField(max_length=200)

    def get_absolute_url(self):
        return reverse('job_detail', args=(self.pk,))

    def __str__(self):
        return f'{self.name}'


class Person(models.Model):
    job = models.ForeignKey(Job, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)

    def get_absolute_url(self):
        return reverse('person_detail', args=(self.pk,))

    def __str__(self):
        return f'{self.first_name} {self.last_name}'
