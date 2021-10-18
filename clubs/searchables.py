from django.db import models
from django.db.models.functions import Concat

from searcher.register import SearchConfig

from .models import Club, ClubMember


class ClubConfig(SearchConfig):
    model = Club

    title_fields = ['name']
    body_fields = ['name']


class ClubMemberConfig(SearchConfig):
    model = ClubMember

    title_fields = ['first_name', 'last_name']
    body_fields = ['first_name', 'last_name']
