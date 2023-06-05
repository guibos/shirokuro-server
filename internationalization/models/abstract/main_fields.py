from django.core.exceptions import ValidationError
from django.db import models

from internationalization.models.abstract.audit import Audit


def _validator(value):
    if type(value) != list:
        raise ValidationError('Invalid type')
    for e in value:
        if type(e) != str:
            raise ValidationError('Invalid type')


class MainFields(Audit):
    source_data = models.URLField(null=True)
    added = models.DateTimeField(null=False)
    deprecated = models.DateTimeField(null=True)

    description = models.JSONField(default=list, validators=[_validator], null=False, blank=False)

    class Meta:
        abstract = True
