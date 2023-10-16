import os


class Pyi18nInfoBase:
    _SEMANTIC_EXTENSION_FILE = '.ttl'
    _SEMANTIC_PREFIX_FILE = '_'
    _SEMANTIC_REGION_DATA_DIR = os.path.join(os.path.dirname(__file__), 'data', 'region')
    _SEMANTIC_LANGUAGE_DATA_DIR = os.path.join(os.path.dirname(__file__), 'data', 'language')
    _SEMANTIC_SCRIPT_DATA_DIR = os.path.join(os.path.dirname(__file__), 'data', 'script')
    _SEMANTIC_VARIANT_DATA_DIR = os.path.join(os.path.dirname(__file__), 'data', 'variant')
    _SEMANTIC_GRANDFATHERED_DATA_DIR = os.path.join(os.path.dirname(__file__), 'data', 'grandfathered')
    _SEMANTIC_REDUNDANT_DATA_DIR = os.path.join(os.path.dirname(__file__), 'data', 'redundant')
