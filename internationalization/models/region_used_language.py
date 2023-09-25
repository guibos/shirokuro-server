from django.db import models
from django.db.models import UniqueConstraint

from internationalization.models.language import Language
from internationalization.models.region import Region


class RegionUsedLanguage(models.Model):
    region = models.ForeignKey(Region, on_delete=models.RESTRICT)
    language = models.ForeignKey(Language, on_delete=models.ForeignKey)

    class Meta:
        constraints = [UniqueConstraint(fields=['region', 'language'], name="uq_region_used_language")]
