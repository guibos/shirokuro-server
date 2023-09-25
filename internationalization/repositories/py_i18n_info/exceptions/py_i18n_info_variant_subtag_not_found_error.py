from internationalization.repositories.py_i18n_info.exceptions.py_i18n_info_tag_or_subtag_not_found_error import \
    Pyi18nInfoTagOrSubtagNotFoundError


class Pyi18nInfoVariantSubtagNotFoundError(Pyi18nInfoTagOrSubtagNotFoundError):
    """Exception raised when a variant subtag is not found."""
    _MESSAGE_TEMPLATE = "Variant subtag not found: '{}'."

    def __init__(self, variant_subtag: str):
        super().__init__(self._MESSAGE_TEMPLATE.format(variant_subtag))
