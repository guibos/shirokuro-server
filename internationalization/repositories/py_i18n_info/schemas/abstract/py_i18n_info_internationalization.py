from typing import Any, Dict, Optional, Union

from pydantic import BaseModel, AnyUrl

from internationalization.repositories.py_i18n_info.schemas.abstract.py_i18n_info_translation import \
    Pyi18nInfoTranslation


class Pyi18nInfoInternationalization(BaseModel):
    id: Optional[Union[str, int]] = None
    source_data: Optional[AnyUrl] = None
    i18n_info: Dict[Any, Pyi18nInfoTranslation] = {}
