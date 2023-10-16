from typing import Union, Type

from internationalization.repositories.py_i18n_info.schemas.py_i18n_info_ext_lang import Pyi18nInfoExtLang
from internationalization.repositories.py_i18n_info.schemas.py_i18n_info_grandfathered import \
    Pyi18nInfoGrandfathered
from internationalization.repositories.py_i18n_info.schemas.py_i18n_info_language import Pyi18nInfoLanguage
from internationalization.repositories.py_i18n_info.schemas.py_i18n_info_redundant import Pyi18nInfoRedundant
from internationalization.repositories.py_i18n_info.schemas.py_i18n_info_region import Pyi18nInfoRegion
from internationalization.repositories.py_i18n_info.schemas.py_i18n_info_script import Pyi18nInfoScript
from internationalization.repositories.py_i18n_info.schemas.py_i18n_info_variant import Pyi18nInfoVariant

SubtagsType = Union[Pyi18nInfoScript, Pyi18nInfoLanguage, Pyi18nInfoExtLang, Pyi18nInfoRegion, Pyi18nInfoVariant]
TagType = Union[Pyi18nInfoGrandfathered, Pyi18nInfoRedundant]
TagsOrSubtags: Type[Pyi18nInfoScript | Pyi18nInfoLanguage | Pyi18nInfoExtLang | Pyi18nInfoRegion | Pyi18nInfoVariant
                    | Pyi18nInfoGrandfathered | Pyi18nInfoRedundant] = Union[SubtagsType, TagType]
