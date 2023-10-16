from typing import List, Optional

from pydantic import ConfigDict, BaseModel

from internationalization.repositories.bcp47.schemas.bcp47_grandfathered import BCP47Grandfathered
from internationalization.repositories.py_i18n_info.schemas.abstract.py_i18n_info_internationalization import \
    Pyi18nInfoInternationalization
from internationalization.repositories.py_i18n_info.schemas.py_i18n_info_language import Pyi18nInfoLanguage
from internationalization.repositories.py_i18n_info.schemas.py_i18n_info_region import Pyi18nInfoRegion
from internationalization.repositories.py_i18n_info.schemas.py_i18n_info_variant import Pyi18nInfoVariant, \
    Pyi18nInfoVariantPrefix


class Pyi18nInfoGrandfatheredPreferredValue(BaseModel):
    language: Pyi18nInfoLanguage
    region: Optional[Pyi18nInfoRegion] = None
    variant: Optional[Pyi18nInfoVariant] = None
    model_config = ConfigDict(extra='forbid')


class Pyi18nInfoGrandfatheredPrefix(Pyi18nInfoVariantPrefix):
    pass


class Pyi18nInfoGrandfathered(BCP47Grandfathered, Pyi18nInfoInternationalization):
    prefix: List['Pyi18nInfoGrandfatheredPrefix'] = []
    preferred_value: Optional['Pyi18nInfoGrandfatheredPreferredValue'] = None
