import os.path


class BCP47Base:
    _LANGUAGE_SUBTAG_REGISTRY_FILE_PATH = os.path.join(os.path.dirname(__file__), 'data', 'language-subtag-registry',
                                                       'language-subtag-registry')
