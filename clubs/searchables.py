from django.urls import reverse
from searcher.register import SearchConfig

from .models import Club, ClubMember


class ClubConfig(SearchConfig):
    model = Club

    title_fields = ['name']
    body_fields = ['name']

    @staticmethod
    def get_instance_url(instance, request):
        return reverse('club_detail', args=(instance.pk,))


class ClubMemberConfig(SearchConfig):
    model = ClubMember

    title_fields = ['first_name', 'last_name']
    body_fields = ['first_name', 'last_name']

    @staticmethod
    def get_instance_url(instance, request):
        return reverse('clubmember_detail', args=(instance.pk,))
