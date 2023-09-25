from django.db import models

from internationalization.models.abstract.subtag import Subtag
from internationalization.models.language_scope import LanguageScope
from internationalization.models.script import Script


class Language(Subtag):
    comments = models.TextField(null=True)
    preferred_value_language = models.ForeignKey('self', on_delete=models.RESTRICT, null=True)
    macro_language = models.ForeignKey('self', on_delete=models.RESTRICT, null=True, related_name='macro_language_back')
    scope = models.ForeignKey(LanguageScope, on_delete=models.RESTRICT, null=True)
    suppress_script = models.ForeignKey(Script, on_delete=models.RESTRICT, null=True)
    iso_639_1 = models.CharField(max_length=2, unique=True)
    iso_639_2 = models.CharField(max_length=3, unique=True)
    iso_639_3 = models.CharField(max_length=3, unique=True)
    iso_639_5 = models.CharField(max_length=3, unique=True)
