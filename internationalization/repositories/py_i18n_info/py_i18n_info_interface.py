import abc
from typing import List, Iterable, Dict, Union

from internationalization.enums.bcp47_type import BCP47Type
from internationalization.enums.language_scope import LanguageScopeEnum
from internationalization.repositories.bcp47.exceptions.ext_lang_subtag_not_found_error import \
    ExtLangSubtagNotFoundError
from internationalization.repositories.bcp47.exceptions.grandfathered_tag_not_found_error import \
    GrandfatheredTagNotFoundError
from internationalization.repositories.bcp47.exceptions.language_scope_not_found_error import LanguageScopeNotFoundError
from internationalization.repositories.bcp47.exceptions.language_subtag_not_found_error import \
    LanguageSubtagNotFoundError
from internationalization.repositories.bcp47.exceptions.redundant_tag_not_found_error import RedundantTagNotFoundError
from internationalization.repositories.bcp47.exceptions.region_subtag_not_found_error import RegionSubtagNotFoundError
from internationalization.repositories.bcp47.exceptions.script_subtag_not_found_error import ScriptSubtagNotFoundError
from internationalization.repositories.bcp47.exceptions.tag_or_subtag_not_found_error import TagOrSubtagNotFoundError
from internationalization.repositories.bcp47.exceptions.variant_subtag_not_found_error import VariantSubtagNotFoundError
from internationalization.repositories.bcp47.schemas.abstract.subtag_data_finder import SubtagDataFinder
from internationalization.repositories.py_i18n_info.schemas.py_i18n_info_ext_lang import Pyi18nInfoExtLang
from internationalization.repositories.py_i18n_info.schemas.py_i18n_info_grandfathered import Pyi18nInfoGrandfathered
from internationalization.repositories.py_i18n_info.schemas.py_i18n_info_language import Pyi18nInfoLanguage
from internationalization.repositories.py_i18n_info.schemas.py_i18n_info_language_scope import Pyi18nInfoLanguageScope
from internationalization.repositories.py_i18n_info.schemas.py_i18n_info_redundant import Pyi18nInfoRedundant
from internationalization.repositories.py_i18n_info.schemas.py_i18n_info_region import Pyi18nInfoRegion
from internationalization.repositories.py_i18n_info.schemas.py_i18n_info_script import Pyi18nInfoScript
from internationalization.repositories.py_i18n_info.schemas.py_i18n_info_subtags import Pyi18nInfoSubtags
from internationalization.repositories.py_i18n_info.schemas.py_i18n_info_variant import Pyi18nInfoVariant
from internationalization.repositories.py_i18n_info.type_aliases import TagsOrSubtags


class Pyi18nInfoInterface:

    def __init__(self):
        super().__init__()
        self._TAG_OR_SUBTAG_DATA_FINDER = [
            SubtagDataFinder(self.get_language_by_subtag, BCP47Type.LANGUAGE),
            SubtagDataFinder(self.get_ext_lang_by_subtag, BCP47Type.EXTLANG),
            SubtagDataFinder(self.get_script_by_subtag, BCP47Type.SCRIPT),
            SubtagDataFinder(self.get_region_by_subtag, BCP47Type.REGION),
            SubtagDataFinder(self.get_variant_by_subtag, BCP47Type.VARIANT)
        ]

    @property
    @abc.abstractmethod
    def languages(self) -> List[Pyi18nInfoLanguage]:
        pass

    def get_language_by_subtag(self, subtag: str, case_sensitive: bool = False) -> Pyi18nInfoLanguage:
        try:
            return self._tag_or_subtag_filter(subtag, self.languages, case_sensitive)
        except TagOrSubtagNotFoundError as e:
            raise LanguageSubtagNotFoundError(subtag) from e

    @property
    @abc.abstractmethod
    def languages_scopes(self) -> Iterable[Pyi18nInfoLanguageScope]:
        pass

    def get_language_scope_by_name(self, name: str) -> Pyi18nInfoLanguageScope:
        try:
            langauge_scope_enum = LanguageScopeEnum(name)
        except ValueError as e:
            raise LanguageScopeNotFoundError(name) from e
        for bcp47_language_scope in self.languages_scopes:
            if langauge_scope_enum == bcp47_language_scope.scope:
                return bcp47_language_scope

        raise RuntimeError(f'Unexpected workflow error to find a language scope: "{name}"')

    @property
    @abc.abstractmethod
    def ext_langs(self) -> List[Pyi18nInfoExtLang]:
        pass

    def get_ext_lang_by_subtag(self, subtag: str, case_sensitive: bool = False) -> Pyi18nInfoExtLang:
        try:
            return self._tag_or_subtag_filter(subtag, self.ext_langs, case_sensitive)
        except TagOrSubtagNotFoundError as e:
            raise ExtLangSubtagNotFoundError(subtag) from e

    @property
    @abc.abstractmethod
    def scripts(self) -> List[Pyi18nInfoScript]:
        pass

    def get_script_by_subtag(self, subtag: str, case_sensitive: bool = False) -> Pyi18nInfoScript:
        try:
            return self._tag_or_subtag_filter(subtag, self.scripts, case_sensitive)
        except TagOrSubtagNotFoundError as e:
            raise ScriptSubtagNotFoundError(subtag) from e

    @property
    @abc.abstractmethod
    def regions(self) -> List[Pyi18nInfoRegion]:
        pass

    def get_region_by_subtag(self, subtag: str, case_sensitive: bool = False) -> Pyi18nInfoRegion:
        try:
            return self._tag_or_subtag_filter(subtag, self.regions, case_sensitive)
        except TagOrSubtagNotFoundError as e:
            raise RegionSubtagNotFoundError(subtag) from e

    @property
    @abc.abstractmethod
    def variants(self) -> List[Pyi18nInfoVariant]:
        pass

    def get_variant_by_subtag(self, subtag: str, case_sensitive: bool = False) -> Pyi18nInfoVariant:
        try:
            return self._tag_or_subtag_filter(subtag, self.variants, case_sensitive)
        except TagOrSubtagNotFoundError as e:
            raise VariantSubtagNotFoundError(subtag) from e

    @property
    @abc.abstractmethod
    def grandfathered(self) -> List[Pyi18nInfoGrandfathered]:
        pass

    def get_grandfathered_by_tag(self, tag: str, case_sensitive: bool = False) -> Pyi18nInfoGrandfathered:
        try:
            return self._tag_or_subtag_filter(tag, self.variants, case_sensitive)
        except TagOrSubtagNotFoundError as e:
            raise GrandfatheredTagNotFoundError(tag) from e

    @property
    @abc.abstractmethod
    def redundant(self) -> List[Pyi18nInfoRedundant]:
        pass

    def get_redundant_by_tag(self, tag: str, case_sensitive: bool = False) -> Pyi18nInfoRedundant:
        try:
            return self._tag_or_subtag_filter(tag, self.variants, case_sensitive)
        except TagOrSubtagNotFoundError as e:
            raise RedundantTagNotFoundError(tag) from e

    def _tag_or_subtag_filter(self, subtag_str: str, tag_or_subtag_list: List[TagsOrSubtags],
                              case_sensitive: bool) -> TagsOrSubtags:
        if not case_sensitive:
            subtag_str = subtag_str.lower()
        for subtag in tag_or_subtag_list:
            tag_or_subtag_str = self._get_tag_or_subtag(subtag)
            if not case_sensitive:
                tag_or_subtag_str = tag_or_subtag_str.lower()
            if subtag_str == tag_or_subtag_str:
                return subtag
        raise TagOrSubtagNotFoundError(subtag_str)

    def tag_or_subtag_parser(self, tag_or_subtag: str, case_sensitive=False) -> Pyi18nInfoSubtags:
        return Pyi18nInfoSubtags(**self._tag_or_subtag_parser(tag_or_subtag, case_sensitive))

    def _tag_or_subtag_parser(
        self, tag_or_subtag: str, case_sensitive: bool
    ) -> Dict[str, Union[Pyi18nInfoLanguage, Pyi18nInfoExtLang, Pyi18nInfoScript, Pyi18nInfoRegion, Pyi18nInfoVariant,
                         Pyi18nInfoExtLang]]:
        i = 0
        tag_or_subtag_data = {}
        for subtag in tag_or_subtag.split('-'):
            while True:
                if i >= len(self._TAG_OR_SUBTAG_DATA_FINDER):
                    raise TagOrSubtagNotFoundError(f"Subtag {subtag} of {tag_or_subtag} is not found.")
                try:
                    tag_or_subtag_data[self._TAG_OR_SUBTAG_DATA_FINDER[i].data_dict_key.
                                       value] = self._TAG_OR_SUBTAG_DATA_FINDER[i].callable(subtag, case_sensitive)
                    break
                except TagOrSubtagNotFoundError:
                    i += 1
                    continue
        return tag_or_subtag_data

    @staticmethod
    def _get_tag_or_subtag(model: TagsOrSubtags) -> str:
        if str_tag_or_subtag := getattr(model, 'subtag', ''):
            return str_tag_or_subtag
        elif str_tag_or_subtag := getattr(model, 'tag', ''):
            return str_tag_or_subtag
        raise RuntimeError("Tag or subtag not found.")
