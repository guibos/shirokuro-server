from internationalization.repositories.py_i18n_info.exceptions.py_i18n_info_tag_or_subtag_not_found_error import \
    Pyi18nInfoTagOrSubtagNotFoundError


class Pyi18nInfoGrandfatheredTagNotFoundError(Pyi18nInfoTagOrSubtagNotFoundError):
    """Exception raised when a grandfathered tag is not found."""
    _MESSAGE_TEMPLATE = "Grandfathered tag not found: '{}'."

    def __init__(self, grandfathered_tag: str):
        super().__init__(self._MESSAGE_TEMPLATE.format(grandfathered_tag))
