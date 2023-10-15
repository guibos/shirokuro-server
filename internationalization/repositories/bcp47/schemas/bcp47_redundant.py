from datetime import datetime
from typing import Optional

from pydantic import ConfigDict, BaseModel

from internationalization.repositories.bcp47.schemas.abstract.bcp47_tag import BCP47Tag
from internationalization.repositories.bcp47.schemas.abstract.preferred_value_validator import PreferredValueValidator
from internationalization.repositories.bcp47.schemas.bcp47_language import BCP47Language
from internationalization.repositories.bcp47.schemas.bcp47_script import BCP47Script


class BCP47RedundantPreferredValue(BaseModel):
    language: BCP47Language
    script: Optional[BCP47Script] = None
    model_config = ConfigDict(extra='forbid')


class BCP47Redundant(BCP47Tag, PreferredValueValidator):
    preferred_value: Optional[BCP47RedundantPreferredValue] = None
    deprecated: Optional[datetime] = None
