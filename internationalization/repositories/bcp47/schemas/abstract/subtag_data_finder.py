import dataclasses
from typing import Callable, Any

from internationalization.enums.bcp47_type import BCP47Type


@dataclasses.dataclass
class SubtagDataFinder:
    callable: Callable[[str, bool], Any]
    data_dict_key: BCP47Type
