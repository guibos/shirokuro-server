from internationalization.repositories.bcp47.exceptions.tag_or_subtag_not_found_error import TagOrSubtagNotFoundError


class RegionSubtagNotFoundError(TagOrSubtagNotFoundError):
    """Exception raised when a region subtag is not found."""
    _MESSAGE_TEMPLATE = "Region subtag not found: '{}'."

    def __init__(self, region_subtag: str):
        super().__init__(self._MESSAGE_TEMPLATE.format(region_subtag))
