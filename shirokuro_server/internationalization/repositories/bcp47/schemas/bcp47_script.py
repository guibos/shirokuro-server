from typing import Optional

from internationalization.repositories.bcp47.schemas.abstract.bcp47_subtag import BCP47Subtag


class BCP47Script(BCP47Subtag):
    comments: Optional[str] = None
