from enum import Enum


class BCP47Type(Enum):
    LANGUAGE = 'language'
    SCRIPT = 'script'
    REGION = 'region'
    VARIANT = 'variant'
    GRANDFATHERED = 'grandfathered'
    REDUNDANT = 'redundant'
    EXTLANG = 'extlang'
