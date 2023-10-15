from typing import Optional, List

from pydantic import ConfigDict, BaseModel

from internationalization.repositories.bcp47.schemas.bcp47_region import BCP47Region
from internationalization.repositories.py_i18n_info.schemas.abstract.py_i18n_info_internationalization import \
    Pyi18nInfoInternationalization
from internationalization.repositories.py_i18n_info.schemas.py_i18n_info_language import Pyi18nInfoLanguage


class Pyi18nInfoRegion(BCP47Region, Pyi18nInfoInternationalization):
    preferred_value: 'Optional[Pyi18nInfoRegionPreferredValue]'
    iso3166_1_alpha2: Optional[str] = None
    iso3166_1_alpha3: Optional[str] = None
    iso3166_1_numeric: Optional[int] = None
    official_languages: List[Pyi18nInfoLanguage]
    used_languages: List[Pyi18nInfoLanguage]


class Pyi18nInfoRegionPreferredValue(BaseModel):
    region: Pyi18nInfoRegion
    model_config = ConfigDict(extra='forbid')


Pyi18nInfoRegion.model_rebuild()
