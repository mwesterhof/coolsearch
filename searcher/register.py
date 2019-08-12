class SearchField:
    def __init__(self, name, expression=None):
        self.name = name
        self.expression = expression


class ModelIndex:
    def __init__(self):
        self._index = []

    def _get_result_queryset(self, line, body):
        model, fields = line
        annotation_dict = {
            field.name: field.expression
            for field in fields
            if field.expression
        }

        qs = model.objects.annotate(**annotation_dict).filter(
            body=body).values(*[field.name for field in fields])
        return qs

    def add(self, model):
        self._index.append(model)

    def get_union(self, body):
        if self._index:
            first_line, *lines = self._index
            result = self._get_result_queryset(first_line, body)
            for entry in lines:
                result = result.union(self._get_result_queryset(entry, body))

        return result


modelindex = ModelIndex()


def searchable(model):
    search_fields = getattr(model, 'search_fields', [])
    if search_fields:
        for search_field in search_fields:
            search_field.model = model
        modelindex.add((model, search_fields))
    return model
