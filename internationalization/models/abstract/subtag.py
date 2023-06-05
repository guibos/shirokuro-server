from django.db import models

from internationalization.models.abstract.main_fields import MainFields


class Subtag(MainFields):
    subtag = models.CharField(max_length=4, unique=True)

    class Meta:
        abstract = True
