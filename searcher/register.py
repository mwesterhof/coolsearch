from django.apps.registry import apps
from django.db.models import CharField, Q, Value


class ModelIndex:
    def __init__(self):
        self._index = []

    def _search_for_config(self, config, query):
        model = config.model
        annotations = {
            'type': Value(model._meta.verbose_name, output_field=CharField())
        }
        if config.title:
            annotations['title'] = config.title
        if config.body:
            annotations['body'] = config.body

        return model.objects.annotate(**annotations).filter(
            Q(body__icontains=query) | Q(title__icontains=query)).values(
                'title', 'body', 'type')

    def register(self, config):
        self._index.append(config)

    def search(self, query):
        if not self._index:
            return []

        first_config, *configs = self._index
        result = self._search_for_config(first_config, query)
        for config in configs:
            partial = self._search_for_config(config, query)
            result = result.union(partial)

        return result


class SearchConfigMeta(type):
    def __new__(cls, name, bases, dct):
        result = super().__new__(cls, name, bases, dct)

        if bases:
            modelindex.register(result)

        return result


class SearchConfig(metaclass=SearchConfigMeta):
    title = None
    body = None


def import_configs():
    def try_searchables_import(module):
        import_path = '.'.join([module.name, 'searchables'])
        try:
            __import__(import_path)
        except (ModuleNotFoundError, ImportError):
            pass

    for _, module in apps.app_configs.items():
        try_searchables_import(module)


modelindex = ModelIndex()
