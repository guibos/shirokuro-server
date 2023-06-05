from internationalization.repositories.bcp47.exceptions.tag_or_subtag_not_found_error import TagOrSubtagNotFoundError


class LanguageSubtagNotFoundError(TagOrSubtagNotFoundError):
    """Exception raised when a language subtag is not found."""
    _MESSAGE_TEMPLATE = "Language subtag not found: '{}'."

    def __init__(self, language_subtag: str):
        super().__init__(self._MESSAGE_TEMPLATE.format(language_subtag))
