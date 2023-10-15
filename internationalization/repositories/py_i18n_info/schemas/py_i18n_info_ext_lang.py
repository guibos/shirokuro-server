from typing import Optional, List

from pydantic import ConfigDict, BaseModel, field_validator
from pydantic_core.core_schema import ValidationInfo

from internationalization.repositories.bcp47.schemas.bcp47_ext_lang import BCP47ExtLang
from internationalization.repositories.py_i18n_info.schemas.abstract.py_i18n_info_internationalization import \
    Pyi18nInfoInternationalization
from internationalization.repositories.py_i18n_info.schemas.py_i18n_info_language import Pyi18nInfoLanguage


class Pyi18nInfoExtLangPreferredValue(BaseModel):
    language: Optional[Pyi18nInfoLanguage] = None
    model_config = ConfigDict(extra='forbid')


class Pyi18nInfoExtLangPrefix(BaseModel):
    language: Pyi18nInfoLanguage

    @property
    def tag(self) -> str:
        return self.language.subtag
    model_config = ConfigDict(extra='forbid')


class Pyi18nInfoExtLang(BCP47ExtLang, Pyi18nInfoInternationalization):
    prefix: List[Pyi18nInfoExtLangPrefix] = []
    macro_language: Optional[Pyi18nInfoLanguage] = None
    preferred_value: Pyi18nInfoExtLangPreferredValue

    @field_validator('preferred_value')
    def preferred_value_subtag_validator(cls, value: BCP47ExtLang, validation_info: ValidationInfo):
        if value.language.subtag != validation_info.data['subtag']:
            raise ValueError('Preferred_value must be equal than subtag. In the moment of writing this validation all'
                             'extension languages are languages, so, it is possible that this validation it is not '
                             'necessary any more and it is required to check how internationalize extension languages.')

        return value
