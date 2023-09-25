from datetime import datetime
from typing import List

from pydantic import BaseModel


class BCP47Base(BaseModel):
    description: List[str] = []
    added: datetime
    updated_at: datetime

    class Config:
        extra = 'forbid'
