from internationalization.repositories.py_i18n_info.exceptions.py_i18n_info_tag_or_subtag_not_found_error import \
    Pyi18nInfoTagOrSubtagNotFoundError


class Pyi18nInfoRedundantTagNotFoundError(Pyi18nInfoTagOrSubtagNotFoundError):
    """Exception raised when a redundant tag is not found."""
    _MESSAGE_TEMPLATE = "Redundant tag not found: '{}'."

    def __init__(self, redundant_tag: str):
        super().__init__(self._MESSAGE_TEMPLATE.format(redundant_tag))
