from django.contrib.contenttypes.models import ContentType
from django.shortcuts import get_object_or_404
from django.views.generic import RedirectView

from .register import modelindex


class GenericObjectServe(RedirectView):
    permanent = False

    def get_redirect_url(self, *args, **kwargs):
        content_type_pk = self.kwargs['content_type_pk']
        pk = self.kwargs['pk']

        model = get_object_or_404(
            ContentType, pk=content_type_pk).model_class()
        instance = get_object_or_404(model, pk=pk)
        config = modelindex._find_config_for_model(model)
        if hasattr(config, 'get_instance_url'):
            return config.get_instance_url(instance, self.request)

        return instance.get_absolute_url()
