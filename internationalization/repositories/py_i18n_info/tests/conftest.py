from datetime import datetime
from typing import List

import pytest

from internationalization.enums.language_scope import LanguageScopeEnum
from internationalization.repositories.bcp47.bcp47_interface import BCP47Interface
from internationalization.repositories.bcp47.schemas.bcp47_ext_lang import BCP47ExtLang, BCP47ExtLangPrefix, \
    BCP47ExtLangPreferredValue
from internationalization.repositories.bcp47.schemas.bcp47_grandfathered import BCP47Grandfathered
from internationalization.repositories.bcp47.schemas.bcp47_language import BCP47LanguagePreferredValue, BCP47Language
from internationalization.repositories.bcp47.schemas.bcp47_language_scope import BCP47LanguageScope
from internationalization.repositories.bcp47.schemas.bcp47_redundant import BCP47Redundant
from internationalization.repositories.bcp47.schemas.bcp47_region import BCP47Region
from internationalization.repositories.bcp47.schemas.bcp47_script import BCP47Script
from internationalization.repositories.bcp47.schemas.bcp47_variant import BCP47Variant
from internationalization.repositories.py_i18n_info.py_i18n_info_interface import Pyi18nInfoInterface
from internationalization.repositories.py_i18n_info.py_i18n_info_repository import Pyi18nInfoRepository


class BCP47Mock(BCP47Interface):

    def __init__(self):
        super().__init__()

        script_latin = BCP47Script(description=['Latin'],
                                   added=datetime(2005, 10, 16, 0, 0),
                                   updated_at=datetime(2023, 8, 2, 0, 0),
                                   subtag='Latn',
                                   comments=None)

        script_fake = BCP47Script(
            description=['Fake script', 'Another Fake Script'],
            added=datetime(2017, 1, 13, 0, 0),
            updated_at=datetime(2023, 8, 2, 0, 0),
            subtag='Fake',
            comments="Fake script to test",
        )

        language_scope_macro_language = BCP47LanguageScope(scope=LanguageScopeEnum.MACRO_LANGUAGE)
        language_scope_collection = BCP47LanguageScope(scope=LanguageScopeEnum.COLLECTION)

        language_english = BCP47Language(description=['English'],
                                         added=datetime(2005, 10, 16, 0, 0),
                                         deprecated=None,
                                         updated_at=datetime(2023, 8, 2, 0, 0),
                                         subtag='en',
                                         macro_language=None,
                                         scope=None,
                                         comments=None,
                                         suppress_script=script_latin,
                                         preferred_value=None)

        language_austro_asiatic = BCP47Language(description=['Austro-Asiatic languages'],
                                                added=datetime(2009, 7, 29, 0, 0),
                                                updated_at=datetime(2023, 8, 2, 0, 0),
                                                subtag='aav',
                                                macro_language=None,
                                                scope=language_scope_collection,
                                                comments=None,
                                                suppress_script=None,
                                                preferred_value=None,
                                                deprecated=None)

        language_fake = BCP47Language(description=['Fake Language', 'Fake Language D'],
                                      added=datetime(2005, 10, 16, 0, 0),
                                      updated_at=datetime(2023, 8, 2, 0, 0),
                                      subtag='f1',
                                      macro_language=language_austro_asiatic,
                                      scope=None,
                                      comments="Fake language to test",
                                      suppress_script=None,
                                      preferred_value=BCP47LanguagePreferredValue(language=language_english),
                                      deprecated=datetime(2023, 8, 2, 0, 0))

        ext_lang_1 = BCP47ExtLang(description=['Ext lang 1'],
                                  added=datetime(2009, 7, 29, 0, 0),
                                  deprecated=None,
                                  updated_at=datetime(2023, 8, 2, 0, 0),
                                  subtag='en',
                                  preferred_value=BCP47ExtLangPreferredValue(language=language_english),
                                  prefix=[],
                                  macro_language=None)

        ext_lang_2 = BCP47ExtLang(
            description=['Ext lang 2', '2'],
            added=datetime(2009, 7, 29, 0, 0),
            deprecated=datetime(2010, 7, 29, 0, 0),
            updated_at=datetime(2023, 8, 2, 0, 0),
            subtag='f1',
            preferred_value=BCP47ExtLangPreferredValue(language=language_fake),
            prefix=[BCP47ExtLangPrefix(language=language_fake),
                    BCP47ExtLangPrefix(language=language_austro_asiatic)],
            macro_language=language_austro_asiatic)

        region_united_kingdom = BCP47Region(
            description=['United Kingdom'],
            added=datetime(2005, 10, 16, 0, 0),
            deprecated=None,
            updated_at=datetime(2023, 8, 2, 0, 0),
            subtag='GB',
            comments='as of 2006-03-29 GB no longer includes the Channel Islands and Isle of Man; see GG, JE, IM',
            preferred_value=None)
        #
        # variant_english_oxford = BCP47Variant(description=['Oxford English Dictionary spelling'],
        #                                       added=datetime(2015, 4, 17, 0, 0),
        #                                       deprecated=None,
        #                                       updated_at=datetime(2023, 8, 2, 0, 0),
        #                                       subtag='oxendict',
        #                                       prefix=[
        #                                           BCP47VariantPrefix(language=language_english,
        #                                                              ext_lang=None,
        #                                                              script=None,
        #                                                              region=None,
        #                                                              variant=None)
        #                                       ],
        #                                       comments=None,
        #                                       preferred_value=None)
        #
        # grandfathered_english_oxford = BCP47Grandfathered(description=['English, Oxford English Dictionary spelling'],
        #                                                   added=datetime(2003, 7, 9, 0, 0),
        #                                                   deprecated=datetime(2015, 4, 17, 0, 0),
        #                                                   updated_at=datetime(2023, 8, 2, 0, 0),
        #                                                   tag='en-GB-oed',
        #                                                   prefix=[],
        #                                                   comments=None,
        #                                                   preferred_value=BCP47GrandfatheredPreferredValue(
        #                                                       language=language_english,
        #                                                       region=region_united_kingdom,
        #                                                       variant=variant_english_oxford))
        #
        # redundant_british_sign_language = BCP47Redundant(description=['British Sign Language'],
        #                                                  added=datetime(2001, 3, 2, 0, 0),
        #                                                  deprecated=datetime(2009, 7, 29, 0, 0),
        #                                                  updated_at=datetime(2023, 8, 2, 0, 0),
        #                                                  tag='sgn-GB',
        #                                                  preferred_value=BCP47RedundantPreferredValue(
        #                                                      language=language_british_sign_language, script=None))
        #
        # redundant_german_traditional = BCP47Redundant(
        #     description=['German, traditional orthography'],
        #     added=datetime(2001, 7, 17, 0, 0),
        #     deprecated=None,
        #     updated_at=datetime(2023, 8, 2, 0, 0),
        #     tag='de-1901',
        #     preferred_value=None,
        # )

        self._scripts: List[BCP47Script] = [script_latin, script_fake]
        self._languages_scopes: List[BCP47LanguageScope] = [language_scope_macro_language, language_scope_collection]
        self._languages: List[BCP47Language] = [
            language_english,
            language_austro_asiatic,
            language_fake,
        ]
        self._ext_langs: List[BCP47ExtLang] = [ext_lang_1, ext_lang_2]
        self._regions: List[BCP47Region] = [
            region_united_kingdom,
        ]
        self._variants: List[BCP47Variant] = []
        self._grandfathered: List[BCP47Grandfathered] = []
        self._redundant: List[BCP47Redundant] = []

    @property
    def languages(self):
        return self._languages

    @property
    def languages_scopes(self):
        return self._languages_scopes

    @property
    def ext_langs(self):
        return self._ext_langs

    @property
    def scripts(self):
        return self._scripts

    @property
    def regions(self):
        return self._regions

    @property
    def variants(self):
        return self._variants

    @property
    def grandfathered(self):
        return self._grandfathered

    @property
    def redundant(self):
        return self._redundant


@pytest.fixture(scope="session")
def bcp47_mock() -> BCP47Interface:
    return BCP47Mock()


@pytest.fixture(scope="session")
def py_i18n_info_repository_mock(bcp47_mock: BCP47Interface) -> Pyi18nInfoInterface:
    return Pyi18nInfoRepository(bcp47_mock)
