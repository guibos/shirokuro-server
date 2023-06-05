from django.db import models
from internationalization.models.region import Region

from database.models.abstract.common_fields import CommonFields
from internationalization.models.language import Language
from internationalization.models.script import Script


class LocalizationFields(CommonFields):
    language = models.ForeignKey(Language, null=False, on_delete=models.RESTRICT)
    script = models.ForeignKey(Script, null=False, on_delete=models.RESTRICT)
    region = models.ForeignKey(Region, null=True, on_delete=models.RESTRICT)

    class Meta:
        abstract = True
