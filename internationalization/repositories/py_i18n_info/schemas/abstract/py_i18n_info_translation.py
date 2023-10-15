from typing import Optional

from pydantic import ConfigDict, BaseModel


class Pyi18nInfoTranslation(BaseModel):
    name: str
    description: Optional[str] = None
    model_config = ConfigDict(extra='forbid')
