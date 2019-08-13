from django.db import models
from django.db.models.functions import Concat

from searcher.register import SearchConfig

from .models import Club, ClubMember


class ClubConfig(SearchConfig):
    model = Club

    title = models.F('name')
    body = models.F('name')


class ClubMemberConfig(SearchConfig):
    model = ClubMember

    title = Concat(
        models.F('first_name'), models.Value(' '), models.F('last_name')
    )
    body = Concat(
        models.F('first_name'), models.Value(' '), models.F('last_name'),
        models.Value(' is a member of '), models.F('club__name')
    )
