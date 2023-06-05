from typing import Optional

from pydantic import BaseModel

from internationalization.repositories.bcp47.schemas.bcp47_redundant import BCP47Redundant
from internationalization.repositories.py_i18n_info.schemas.abstract.py_i18n_info_internationalization import \
    Pyi18nInfoInternationalization
from internationalization.repositories.py_i18n_info.schemas.py_i18n_info_language import Pyi18nInfoLanguage
from internationalization.repositories.py_i18n_info.schemas.py_i18n_info_script import Pyi18nInfoScript


class Pyi18nInfoRedundantPreferredValue(BaseModel):
    language: Pyi18nInfoLanguage
    script: Optional[Pyi18nInfoScript] = None

    class Config:
        extra = 'forbid'


class Pyi18nInfoRedundant(BCP47Redundant, Pyi18nInfoInternationalization):
    preferred_value: Optional[Pyi18nInfoRedundantPreferredValue] = None
