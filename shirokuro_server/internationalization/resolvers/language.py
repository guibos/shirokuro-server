import typing

import pycountry
from internationalization.types.language import Language


def get_languages() -> typing.List[Language]:
    pycountry.languages._load()

    return [
        Language(
            alpha_2=language.alpha_2,
            alpha_3=language.alpha_3,
            name=language.name,
            scope=language.scope,
            type=language.type,
        ) for language in pycountry.languages.indices["alpha_2"]
    ]
