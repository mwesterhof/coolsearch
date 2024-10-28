from django.urls import re_path

from .views import GenericObjectServe


urlpatterns = [
    re_path(r'^serve/(?P<content_type_pk>\d+)/(?P<pk>\d+)/$', GenericObjectServe.as_view(), name='searcher_generic_serve'),
]
