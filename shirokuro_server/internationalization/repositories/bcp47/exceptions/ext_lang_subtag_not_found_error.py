from internationalization.repositories.bcp47.exceptions.tag_or_subtag_not_found_error import TagOrSubtagNotFoundError


class ExtLangSubtagNotFoundError(TagOrSubtagNotFoundError):
    """Exception raised when an ext lang subtag is not found."""
    _MESSAGE_TEMPLATE = "Ext lang subtag not found: '{}'."

    def __init__(self, ext_lang_subtag: str):
        super().__init__(self._MESSAGE_TEMPLATE.format(ext_lang_subtag))
