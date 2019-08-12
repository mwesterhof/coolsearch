from django.db.models import CharField, Q, Value


class SearchConfig:
    def __init__(self, title=None, body=None):
        self.title = title
        self.body = body


class ModelIndex:
    def __init__(self):
        self._index = []

    def _search_for_model(self, model, query):
        annotations = {
            'type': Value(model._meta.verbose_name, output_field=CharField())
        }
        search_config = model.search_config
        if search_config.title:
            annotations['title'] = search_config.title
        if search_config.body:
            annotations['body'] = search_config.body

        return model.objects.annotate(**annotations).filter(
            Q(body__icontains=query) | Q(title__icontains=query)).values(
                'title', 'body', 'type')

    def add(self, model):
        self._index.append(model)

    def search(self, query):
        if not self._index:
            return []

        first_model, *models = self._index
        result = self._search_for_model(first_model, query)
        for model in models:
            partial = self._search_for_model(model, query)
            result = result.union(partial)

        return result


modelindex = ModelIndex()


def searchable(model):
    if model.search_config:
        modelindex.add(model)
    return model
