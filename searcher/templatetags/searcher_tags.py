from django.template import Library
from django.urls import reverse

register = Library()


@register.simple_tag
def searcher_url(result):
    content_type_pk = result['_content_type']
    pk = result['id']
    return reverse('searcher_generic_serve', args=(content_type_pk, pk))
