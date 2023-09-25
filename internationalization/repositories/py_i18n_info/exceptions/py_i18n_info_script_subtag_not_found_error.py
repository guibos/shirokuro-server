from internationalization.repositories.py_i18n_info.exceptions.py_i18n_info_tag_or_subtag_not_found_error import \
    Pyi18nInfoTagOrSubtagNotFoundError


class Pyi18nInfoScriptSubtagNotFoundError(Pyi18nInfoTagOrSubtagNotFoundError):
    """Exception raised when a script subtag is not found."""
    _MESSAGE_TEMPLATE = "Script subtag not found: '{}'."

    def __init__(self, script_subtag: str):
        super().__init__(self._MESSAGE_TEMPLATE.format(script_subtag))
