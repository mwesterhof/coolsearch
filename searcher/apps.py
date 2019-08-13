from django.apps import AppConfig

from .register import import_configs


class SearcherConfig(AppConfig):
    name = 'searcher'

    def ready(self, *args, **kwargs):
        import_configs()
