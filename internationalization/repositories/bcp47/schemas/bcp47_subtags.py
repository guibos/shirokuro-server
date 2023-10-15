from typing import Optional

from pydantic import ConfigDict, BaseModel

from internationalization.repositories.bcp47.schemas.bcp47_ext_lang import BCP47ExtLang
from internationalization.repositories.bcp47.schemas.bcp47_language import BCP47Language
from internationalization.repositories.bcp47.schemas.bcp47_region import BCP47Region
from internationalization.repositories.bcp47.schemas.bcp47_script import BCP47Script
from internationalization.repositories.bcp47.schemas.bcp47_variant import BCP47Variant


class BCP47Subtags(BaseModel):
    language: BCP47Language
    ext_lang: Optional[BCP47ExtLang] = None
    script: Optional[BCP47Script] = None
    region: Optional[BCP47Region] = None
    variant: Optional[BCP47Variant] = None

    @property
    def tag(self) -> str:
        return '-'.join((subtag.subtag
                         for subtag in (self.language, self.ext_lang, self.script, self.region, self.variant)
                         if subtag))

    def __hash__(self):
        return hash(str(self.tag))

    def __eq__(self, other):
        return self.tag == other.tag

    model_config = ConfigDict(extra='forbid')
