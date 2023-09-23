from datetime import datetime
from typing import Optional, List

from pydantic import BaseModel

from internationalization.repositories.bcp47.schemas.abstract.bcp47_tag import BCP47Tag
from internationalization.repositories.bcp47.schemas.abstract.preferred_value_validator import PreferredValueValidator
from internationalization.repositories.bcp47.schemas.bcp47_language import BCP47Language
from internationalization.repositories.bcp47.schemas.bcp47_region import BCP47Region
from internationalization.repositories.bcp47.schemas.bcp47_variant import BCP47VariantPrefix, BCP47Variant


class BCP47GrandfatheredPreferredValue(BaseModel):
    language: BCP47Language
    region: Optional[BCP47Region] = None
    variant: Optional[BCP47Variant] = None

    class Config:
        extra = 'forbid'


class BCP47GrandfatheredPrefix(BCP47VariantPrefix):
    pass


class BCP47Grandfathered(BCP47Tag, PreferredValueValidator):
    prefix: List['BCP47GrandfatheredPrefix'] = []
    comments: Optional[str] = None
    preferred_value: Optional['BCP47GrandfatheredPreferredValue'] = None
    deprecated: Optional[datetime] = None
