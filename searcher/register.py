from django.apps.registry import apps
from django.contrib.postgres.search import SearchQuery, SearchRank
from django.db.models import CharField, Value

from .expressions import body_field, title_field


class SearchOptions:
    PARTIAL = 1
    FULL = 2


class ConfigNotFound(Exception):
    pass


class ModelIndex:
    def __init__(self):
        self._index = []

    def _get_contenttype(self, config):
        if not hasattr(config, 'contenttype'):
            ContentType = apps.get_model('contenttypes', 'ContentType')
            config.contenttype = ContentType.objects.get_for_model(
                config.model)
        return config.contenttype.pk

    def _search_for_config(self, config, query, search_type):
        content_type = self._get_contenttype(config)

        model = config.model
        annotations = {
            '_type': Value(model._meta.verbose_name, output_field=CharField()),
            '_content_type': Value(content_type, output_field=CharField()),
            '_title': config.title,
            '_body': config.body,
            '_rank': SearchRank(config.body, query),
        }

        qs = config.get_queryset().annotate(**annotations)
        if search_type == SearchOptions.PARTIAL:
            filtered = qs.filter(_body__contains=query.value)
        else:
            filtered = qs.filter(_body=query.value)

        return filtered.values(
            'id', '_title', '_type', '_content_type', '_rank')

    def _find_config_for_model(self, model):
        for config in self._index:
            if config.model is model:
                return config

        raise ConfigNotFound(model)

    def register(self, config):
        self._index.append(config)

    def search(self, query, search_type=SearchOptions.PARTIAL):
        if not self._index:
            return []

        query_obj = SearchQuery(query)
        first_config, *configs = self._index
        result = self._search_for_config(first_config, query_obj, search_type)
        for config in configs:
            partial = self._search_for_config(config, query_obj, search_type)
            result = result.union(partial)

        return result


class SearchConfigMeta(type):
    def __new__(cls, name, bases, dct):
        if bases:
            # concatenated title field
            dct['title'] = title_field(dct['title_fields'])
            # searchable body field
            dct['body'] = body_field(dct['body_fields'])

        result = super().__new__(cls, name, bases, dct)

        if bases:
            modelindex.register(result)

        return result


class SearchConfig(metaclass=SearchConfigMeta):
    title = None
    body = None

    @classmethod
    def get_queryset(cls):
        return cls.model.objects.all()


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
