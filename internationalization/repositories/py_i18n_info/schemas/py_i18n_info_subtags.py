from typing import Optional

from internationalization.repositories.bcp47.schemas.bcp47_subtags import BCP47Subtags
from internationalization.repositories.py_i18n_info.schemas.py_i18n_info_ext_lang import Pyi18nInfoExtLang
from internationalization.repositories.py_i18n_info.schemas.py_i18n_info_language import Pyi18nInfoLanguage
from internationalization.repositories.py_i18n_info.schemas.py_i18n_info_region import Pyi18nInfoRegion
from internationalization.repositories.py_i18n_info.schemas.py_i18n_info_script import Pyi18nInfoScript
from internationalization.repositories.py_i18n_info.schemas.py_i18n_info_variant import Pyi18nInfoVariant


class Pyi18nInfoSubtags(BCP47Subtags):
    language: Pyi18nInfoLanguage
    ext_lang: Optional[Pyi18nInfoExtLang] = None
    script: Optional[Pyi18nInfoScript] = None
    region: Optional[Pyi18nInfoRegion] = None
    variant: Optional[Pyi18nInfoVariant] = None
