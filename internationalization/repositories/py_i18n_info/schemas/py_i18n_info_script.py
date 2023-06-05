from internationalization.repositories.bcp47.schemas.bcp47_script import BCP47Script
from internationalization.repositories.py_i18n_info.schemas.abstract.py_i18n_info_internationalization import \
    Pyi18nInfoInternationalization


class Pyi18nInfoScript(BCP47Script, Pyi18nInfoInternationalization):
    pass
