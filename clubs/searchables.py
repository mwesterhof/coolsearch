from django.db import models
from django.db.models.functions import Concat

from searcher.register import fields, SearchConfig

from .models import Club, ClubMember


class ClubConfig(SearchConfig):
    model = Club

    title = fields('name')
    body = fields('name')


class ClubMemberConfig(SearchConfig):
    model = ClubMember

    title = fields('first_name', 'last_name')
    body = Concat(
        models.F('first_name'), models.Value(' '), models.F('last_name'),
        models.Value(' is a member of '), models.F('club__name')
    )
