from django.db import models

from internationalization.models.abstract.audit import Audit


class LanguageScope(Audit):
    description = models.TextField(unique=True)
