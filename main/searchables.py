from searcher.register import SearchConfig

from .models import Job, Person


class JobConfig(SearchConfig):
    model = Job

    title_fields = ['name']
    body_fields = ['name']

    @staticmethod
    def get_instance_url(instance, request):
        return reverse('job_detail', args=(instance.pk,))


class PersonConfig(SearchConfig):
    model = Person

    title_fields = ['first_name']
    body_fields = ['first_name', 'last_name']

    @staticmethod
    def get_instance_url(instance, request):
        return reverse('person_detail', args=(instance.pk,))

    @classmethod
    def get_queryset(cls):
        return Person.objects.filter(is_active=True)
