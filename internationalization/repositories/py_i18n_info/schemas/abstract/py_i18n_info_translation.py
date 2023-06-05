from typing import Optional

from pydantic import BaseModel


class Pyi18nInfoTranslation(BaseModel):
    name: str
    description: Optional[str] = None

    class Config:
        extra = 'forbid'
