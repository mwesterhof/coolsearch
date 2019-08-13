from django.db import models
from django.db.models.functions import Concat


def fields(*names):
    if len(names) == 1:
        return models.F(names[0])

    values = []
    for name in names:
        values.extend([
            models.F(name),
            models.Value(' ')
        ])
    values.pop(-1)

    return Concat(*values, output_field=models.CharField())
