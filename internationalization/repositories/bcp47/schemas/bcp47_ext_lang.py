from datetime import datetime
from typing import List, Optional

from pydantic import ConfigDict, BaseModel, field_validator
from pydantic_core.core_schema import ValidationInfo

from internationalization.repositories.bcp47.schemas.abstract.bcp47_subtag import BCP47Subtag
from internationalization.repositories.bcp47.schemas.bcp47_language import BCP47Language


class BCP47ExtLangPreferredValue(BaseModel):
    language: Optional[BCP47Language] = None
    model_config = ConfigDict(extra='forbid')


class BCP47ExtLangPrefix(BaseModel):
    language: BCP47Language

    @property
    def tag(self) -> str:
        return self.language.subtag
    model_config = ConfigDict(extra='forbid')


class BCP47ExtLang(BCP47Subtag):
    preferred_value: BCP47ExtLangPreferredValue
    prefix: List[BCP47ExtLangPrefix] = []
    macro_language: Optional[BCP47Language] = None
    deprecated: Optional[datetime] = None

    @field_validator('preferred_value')
    def preferred_value_subtag_validator(cls, value: BCP47Language, validation_info: ValidationInfo):
        if value.language.subtag != validation_info.data['subtag']:
            raise ValueError('Preferred_value must be equal than subtag. In the moment of writing this validation all'
                             'extension languages are languages, so, it is possible that this validation it is not '
                             'necessary any more.')
        return value
