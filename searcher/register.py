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
        return config.contenttype.pk

    def _search_for_config(self, config, query):
        content_type = self._get_contenttype(config)

        model = config.model
        annotations = {
            '_type': Value(model._meta.verbose_name, output_field=CharField()),
            '_content_type': Value(content_type, output_field=CharField()),
            '_title': config.title,
            '_body': config.body,
        }

        return config.get_queryset().annotate(**annotations).filter(
            Q(_body__icontains=query) | Q(_title__icontains=query)).values(
                'id', '_title', '_body', '_type', '_content_type')

    def register(self, config):
        self._index.append(config)

    def search(self, query):
        # queryset types matter, the first set should be a vanilla queryset
        # unfortunately, the only way to ensure this is to start with one
        # that's guaranteed to be vanilla and non-empty
        # to get around this, we'll start with a contenttype QS,
        # and exclude those results at the end
        if not self._index:
            return []

        first_config, *configs = self._index
        result = first_config.search(query)
        for config in configs:
            partial = config.search(query)
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
    def search(self, query, **filters):
        registry = modelindex
        content_type = registry._get_contenttype(self)

        model = self.model
        annotations = {
            '_type': Value(model._meta.verbose_name, output_field=CharField()),
            '_content_type': Value(content_type, output_field=CharField()),
            '_title': self.title,
            '_body': self.body,
        }

        return self.get_queryset().filter(**filters).annotate(**annotations).filter(
            Q(_body__icontains=query) | Q(_title__icontains=query)).values(
                'id', '_title', '_body', '_type', '_content_type')

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
