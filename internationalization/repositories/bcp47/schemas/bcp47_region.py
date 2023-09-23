from datetime import datetime
from typing import Optional

from pydantic import BaseModel

from internationalization.repositories.bcp47.schemas.abstract.bcp47_subtag import BCP47Subtag
from internationalization.repositories.bcp47.schemas.abstract.preferred_value_validator import PreferredValueValidator


class BCP47RegionPreferredValue(BaseModel):
    region: 'BCP47Region'

    class Config:
        extra = 'forbid'


class BCP47Region(BCP47Subtag, PreferredValueValidator):
    comments: Optional[str] = None
    preferred_value: Optional[BCP47RegionPreferredValue] = None
    deprecated: Optional[datetime] = None
