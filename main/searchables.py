from searcher.register import SearchConfig

from .models import Job, Person


class JobConfig(SearchConfig):
    model = Job

    title_fields = ['name']
    body_fields = ['name']


class PersonConfig(SearchConfig):
    model = Person

    title_fields = ['first_name']
    body_fields = ['first_name', 'last_name']
