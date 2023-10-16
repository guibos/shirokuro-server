from typing import Optional, List

from pydantic import ConfigDict, BaseModel

from internationalization.repositories.bcp47.schemas.bcp47_variant import BCP47Variant
from internationalization.repositories.py_i18n_info.schemas.abstract.py_i18n_info_internationalization import \
    Pyi18nInfoInternationalization
from internationalization.repositories.py_i18n_info.schemas.py_i18n_info_ext_lang import Pyi18nInfoExtLangPrefix, \
    Pyi18nInfoExtLang
from internationalization.repositories.py_i18n_info.schemas.py_i18n_info_region import Pyi18nInfoRegion
from internationalization.repositories.py_i18n_info.schemas.py_i18n_info_script import Pyi18nInfoScript


class Pyi18nInfoVariantPreferredValue(BaseModel):
    variant: 'BCP47Variant'
    model_config = ConfigDict(extra='forbid')


class Pyi18nInfoVariantPrefix(Pyi18nInfoExtLangPrefix):
    ext_lang: Optional[Pyi18nInfoExtLang] = None
    script: Optional[Pyi18nInfoScript] = None
    region: Optional[Pyi18nInfoRegion] = None
    variant: Optional['Pyi18nInfoVariant'] = None

    @property
    def tag(self) -> str:
        return '-'.join((subtag.subtag
                         for subtag in (self.language, self.ext_lang, self.script, self.region, self.variant)
                         if subtag))


class Pyi18nInfoVariant(BCP47Variant, Pyi18nInfoInternationalization):
    prefix: List[Pyi18nInfoVariantPrefix] = []
    preferred_value: Optional[Pyi18nInfoVariantPreferredValue] = None
    iso_639_6: Optional[str] = None
