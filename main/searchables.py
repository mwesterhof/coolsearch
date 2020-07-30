from searcher.expressions import fields
from searcher.register import SearchConfig

from .models import Job, Person


class JobConfig(SearchConfig):
    model = Job

    title = fields('name')
    body = fields('name')


class PersonConfig(SearchConfig):
    model = Person

    title = fields('first_name', 'last_name')
    body = fields('first_name')
