from internationalization.repositories.py_i18n_info.exceptions.py_i18n_info_tag_or_subtag_not_found_error import \
    Pyi18nInfoTagOrSubtagNotFoundError


class Pyi18nInfoExtLangSubtagNotFoundError(Pyi18nInfoTagOrSubtagNotFoundError):
    """Exception raised when an ext lang subtag is not found."""
    _MESSAGE_TEMPLATE = "Ext lang subtag not found: '{}'."

    def __init__(self, ext_lang_subtag: str):
        super().__init__(self._MESSAGE_TEMPLATE.format(ext_lang_subtag))
