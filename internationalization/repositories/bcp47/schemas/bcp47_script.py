from typing import Optional

from pydantic import BaseModel

from internationalization.repositories.bcp47.schemas.abstract.bcp47_subtag import BCP47Subtag
from internationalization.repositories.bcp47.schemas.abstract.preferred_value_validator import PreferredValueValidator


class BCP47Script(BCP47Subtag):
    comments: Optional[str] = None
