class LanguageScopeNotFoundError(Exception):
    """Exception raised when a language scope is not found."""
    _MESSAGE_TEMPLATE = "Language scope not found: '{}'."

    def __init__(self, language_scope: str):
        super().__init__(self._MESSAGE_TEMPLATE.format(language_scope))
