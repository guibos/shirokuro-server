from datetime import datetime
from typing import Optional

from pydantic import BaseModel

from internationalization.repositories.bcp47.schemas.abstract.bcp47_subtag import BCP47Subtag
from internationalization.repositories.bcp47.schemas.abstract.preferred_value_validator import PreferredValueValidator
from internationalization.repositories.bcp47.schemas.bcp47_language_scope import BCP47LanguageScope
from internationalization.repositories.bcp47.schemas.bcp47_script import BCP47Script


class BCP47LanguagePreferredValue(BaseModel):
    language: 'BCP47Language'

    class Config:
        extra = 'forbid'


class BCP47Language(BCP47Subtag, PreferredValueValidator):
    macro_language: Optional['BCP47Language'] = None
    scope: Optional[BCP47LanguageScope] = None
    comments: Optional[str] = None
    suppress_script: Optional[BCP47Script] = None
    preferred_value: Optional[BCP47LanguagePreferredValue] = None
    deprecated: Optional[datetime] = None
