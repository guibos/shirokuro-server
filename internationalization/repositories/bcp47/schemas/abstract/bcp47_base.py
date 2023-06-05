from datetime import datetime
from typing import Optional, List

from pydantic import BaseModel


class BCP47Base(BaseModel):
    description: List[str] = []
    added: datetime
    deprecated: Optional[datetime] = None
    updated_at: datetime

    class Config:
        extra = 'forbid'
