from typing import Union

from internationalization.repositories.bcp47.schemas.bcp47_ext_lang import BCP47ExtLang, BCP47ExtLangPrefix, \
    BCP47ExtLangPreferredValue
from internationalization.repositories.bcp47.schemas.bcp47_grandfathered import BCP47GrandfatheredPreferredValue, \
    BCP47Grandfathered
from internationalization.repositories.bcp47.schemas.bcp47_language import BCP47Language, \
    BCP47LanguagePreferredValue
from internationalization.repositories.bcp47.schemas.bcp47_redundant import BCP47RedundantPreferredValue, \
    BCP47Redundant
from internationalization.repositories.bcp47.schemas.bcp47_region import BCP47Region, BCP47RegionPreferredValue
from internationalization.repositories.bcp47.schemas.bcp47_script import BCP47Script
from internationalization.repositories.bcp47.schemas.bcp47_variant import BCP47VariantPreferredValue, BCP47Variant

BCP47TagsType = Union[BCP47Grandfathered, BCP47Redundant]
BCP47SubtagsType = Union[BCP47Script, BCP47Language, BCP47Region, BCP47ExtLang, BCP47Variant]
BCP47TagsOrSubtagsType = Union[BCP47TagsType, BCP47SubtagsType]
BCP47PrefixesType = Union[BCP47ExtLangPrefix]
BCP47PreferredValuesType = Union[BCP47LanguagePreferredValue, BCP47RegionPreferredValue, BCP47ExtLangPreferredValue,
                                 BCP47VariantPreferredValue, BCP47GrandfatheredPreferredValue,
                                 BCP47RedundantPreferredValue]
