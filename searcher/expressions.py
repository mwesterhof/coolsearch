from django.db import models
from django.db.models.functions import Cast, Concat


def fields(*names):
    if len(names) == 1:
        return Cast(names[0], output_field=models.CharField(max_length=1000))

    values = []
    for name in names:
        values.extend([
            Cast(name, output_field=models.CharField(max_length=1000)),
            models.Value(' ')
        ])
    values.pop(-1)

    return Concat(*values, output_field=models.CharField())
