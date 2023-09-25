from internationalization.repositories.py_i18n_info.exceptions.py_i18n_info_tag_or_subtag_not_found_error import \
    Pyi18nInfoTagOrSubtagNotFoundError


class Pyi18nInfoLanguageSubtagNotFoundError(Pyi18nInfoTagOrSubtagNotFoundError):
    """Exception raised when a language subtag is not found."""
    _MESSAGE_TEMPLATE = "Language subtag not found: '{}'."

    def __init__(self, language_subtag: str):
        super().__init__(self._MESSAGE_TEMPLATE.format(language_subtag))
