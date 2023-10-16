from pydantic import BaseModel

from internationalization.enums.language_scope import LanguageScopeEnum


class BCP47LanguageScope(BaseModel):
    scope: LanguageScopeEnum
