from django.db import models

from internationalization.models.language import Language
from internationalization.models.abstract.subtag import Subtag


class Region(Subtag):
    preferred_value_region = models.ForeignKey('self', on_delete=models.RESTRICT, null=True)
    iso3166_1_alpha2 = models.CharField(max_length=2, null=True, unique=True)
    iso3166_1_alpha3 = models.CharField(max_length=3, null=True, unique=True)
    iso3166_1_numeric = models.IntegerField(null=True, unique=True)
    official_languages = models.ManyToManyField(Language,
                                                through='RegionOfficialLanguage',
                                                related_name="RegionOfficialLanguage")
    used_languages = models.ManyToManyField(Language, through="RegionUsedLanguage", related_name="RegionUsedLanguage")
    comments = models.TextField(null=True)
