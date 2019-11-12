from searcher import fields, SearchConfig

from django.contrib.contenttypes.models import ContentType


class ContentTypeSearchConfig(SearchConfig):
    model = ContentType
    title = fields('app_label')
    body = fields('app_label')
    _auto_add = False
