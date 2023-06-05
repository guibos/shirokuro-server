from pydantic import model_validator


class PreferredValueValidator:

    @model_validator(mode='before')
    def preferred_value_deprecated_validator(cls, values):
        if values.get('preferred_value') is not None and values.get('deprecated') is None:
            raise ValueError('Preferred_value is set but deprecated is not set')
        return values
