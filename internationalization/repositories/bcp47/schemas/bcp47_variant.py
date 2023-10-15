from datetime import datetime
from typing import List, Optional

from pydantic import ConfigDict, BaseModel

from internationalization.repositories.bcp47.schemas.abstract.bcp47_subtag import BCP47Subtag
from internationalization.repositories.bcp47.schemas.abstract.preferred_value_validator import PreferredValueValidator
from internationalization.repositories.bcp47.schemas.bcp47_ext_lang import BCP47ExtLang, BCP47ExtLangPrefix
from internationalization.repositories.bcp47.schemas.bcp47_region import BCP47Region
from internationalization.repositories.bcp47.schemas.bcp47_script import BCP47Script


class BCP47VariantPreferredValue(BaseModel):
    variant: 'BCP47Variant'
    model_config = ConfigDict(extra='forbid')


class BCP47VariantPrefix(BCP47ExtLangPrefix):
    ext_lang: Optional[BCP47ExtLang] = None
    script: Optional[BCP47Script] = None
    region: Optional[BCP47Region] = None
    variant: Optional['BCP47Variant'] = None

    @property
    def tag(self) -> str:
        return '-'.join((subtag.subtag
                         for subtag in (self.language, self.ext_lang, self.script, self.region, self.variant)
                         if subtag))


class BCP47Variant(BCP47Subtag, PreferredValueValidator):
    prefix: List[BCP47VariantPrefix] = []
    comments: Optional[str] = None
    preferred_value: Optional[BCP47VariantPreferredValue] = None
    deprecated: Optional[datetime] = None
