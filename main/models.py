from django.db import models
from django.db.models.functions import Concat

from searcher.register import searchable, SearchConfig


person_name = Concat(
    models.F('first_name'), models.Value(' '), models.F('last_name')
)
leave_blank = models.Value('', output_field=models.CharField())


@searchable
class Job(models.Model):
    name = models.CharField(max_length=200)

    search_config = SearchConfig(
        title=models.F('name'),
        body=models.F('name'),
    )

    def __str__(self):
        return f'{self.name}'


@searchable
class Person(models.Model):
    job = models.ForeignKey(Job, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)

    search_config = SearchConfig(
        title=person_name,
        body=models.F('first_name')
    )

    def __str__(self):
        return f'{self.first_name} {self.last_name}'
