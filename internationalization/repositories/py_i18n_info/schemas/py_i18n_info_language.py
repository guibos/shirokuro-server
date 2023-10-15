from typing import Optional

from pydantic import ConfigDict, BaseModel

from internationalization.repositories.bcp47.schemas.bcp47_language import BCP47Language
from internationalization.repositories.py_i18n_info.schemas.abstract.py_i18n_info_internationalization import \
    Pyi18nInfoInternationalization
from internationalization.repositories.py_i18n_info.schemas.py_i18n_info_language_scope import Pyi18nInfoLanguageScope
from internationalization.repositories.py_i18n_info.schemas.py_i18n_info_script import Pyi18nInfoScript


class Pyi18nInfoLanguagePreferredValue(BaseModel):
    language: 'Pyi18nInfoLanguage'
    model_config = ConfigDict(extra='forbid')


class Pyi18nInfoLanguage(BCP47Language, Pyi18nInfoInternationalization):
    macro_language: Optional['Pyi18nInfoLanguage'] = None
    scope: Optional[Pyi18nInfoLanguageScope] = None
    suppress_script: Optional[Pyi18nInfoScript] = None
    preferred_value: Optional[Pyi18nInfoLanguagePreferredValue] = None
    iso_639_1: Optional[str] = None
    iso_639_2: Optional[str] = None
    iso_639_3: Optional[str] = None
    iso_639_5: Optional[str] = None
    model_config = ConfigDict(extra='forbid')
