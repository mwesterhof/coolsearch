from django.db import models
from django.db.models.functions import Concat

from searcher.register import SearchConfig

from .models import Job, Person


class JobConfig(SearchConfig):
    model = Job

    title = models.F('name')
    body = models.F('name')


class PersonConfig(SearchConfig):
    model = Person

    title = Concat(
        models.F('first_name'), models.Value(' '), models.F('last_name')
    )
    body = models.F('first_name')
