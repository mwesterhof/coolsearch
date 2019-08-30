from django.apps.registry import apps
from django.db.models import CharField, Q, Value


class ModelIndex:
    def __init__(self):
        self._index = []

    def _get_contenttype(self, config):
        if not hasattr(config, 'contenttype'):
            ContentType = apps.get_model('contenttypes', 'ContentType')
            config.contenttype = ContentType.objects.get_for_model(
                config.model)
        return config.contenttype

    def _search_for_config(self, config, query):
        content_type = self._get_contenttype(config)

        model = config.model
        annotations = {
            '_type': Value(model._meta.verbose_name, output_field=CharField()),
            '_content_type': Value(content_type, output_field=CharField()),
        }
        if config.title:
            annotations['title'] = config.title
        if config.body:
            annotations['body'] = config.body

        return config.get_queryset().annotate(**annotations).filter(
            Q(body__icontains=query) | Q(title__icontains=query)).values(
                'id', 'title', 'body', '_type', '_content_type')

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
