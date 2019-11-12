from django.conf.urls import url

from .views import GenericObjectServe


urlpatterns = [
    url(r'^serve/(?P<content_type_pk>\d+)/(?P<pk>\d+)/$', GenericObjectServe.as_view(), name='searcher_generic_serve'),
]
