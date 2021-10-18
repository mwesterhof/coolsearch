from django.views.generic import DetailView

from .models import Club, ClubMember


class ClubDetail(DetailView):
    model = Club


class ClubMemberDetail(DetailView):
    model = ClubMember
