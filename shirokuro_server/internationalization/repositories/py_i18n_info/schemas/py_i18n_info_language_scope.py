from internationalization.repositories.bcp47.schemas.bcp47_language_scope import BCP47LanguageScope
from internationalization.repositories.py_i18n_info.schemas.abstract.py_i18n_info_internationalization import \
    Pyi18nInfoInternationalization


class Pyi18nInfoLanguageScope(BCP47LanguageScope, Pyi18nInfoInternationalization):
    pass
