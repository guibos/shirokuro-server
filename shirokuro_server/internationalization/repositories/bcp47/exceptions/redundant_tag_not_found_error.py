from internationalization.repositories.bcp47.exceptions.tag_or_subtag_not_found_error import TagOrSubtagNotFoundError


class RedundantTagNotFoundError(TagOrSubtagNotFoundError):
    """Exception raised when a redundant tag is not found."""
    _MESSAGE_TEMPLATE = "Redundant tag not found: '{}'."

    def __init__(self, redundant_tag: str):
        super().__init__(self._MESSAGE_TEMPLATE.format(redundant_tag))
