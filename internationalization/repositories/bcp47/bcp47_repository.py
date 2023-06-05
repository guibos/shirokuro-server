import dataclasses
import functools
from datetime import datetime
from typing import Optional, Dict, Any, Type, List, Union

from internationalization.enums.bcp47_type import BCP47Type
from internationalization.enums.language_scope import LanguageScopeEnum
from internationalization.repositories.bcp47._bcp47_base import BCP47Base
from internationalization.repositories.bcp47.bcp47_interface import BCP47Interface
from internationalization.repositories.bcp47.schemas.abstract.subtag_data_finder import SubtagDataFinder
from internationalization.repositories.bcp47.schemas.bcp47_ext_lang import BCP47ExtLang
from internationalization.repositories.bcp47.schemas.bcp47_grandfathered import BCP47Grandfathered
from internationalization.repositories.bcp47.schemas.bcp47_language import BCP47Language
from internationalization.repositories.bcp47.schemas.bcp47_language_scope import BCP47LanguageScope
from internationalization.repositories.bcp47.schemas.bcp47_redundant import BCP47Redundant
from internationalization.repositories.bcp47.schemas.bcp47_region import BCP47Region
from internationalization.repositories.bcp47.schemas.bcp47_script import BCP47Script
from internationalization.repositories.bcp47.schemas.bcp47_variant import BCP47Variant


@dataclasses.dataclass
class _BCP47ValueAttributes:
    value_type: Type
    internal_name: str


class BCP47Repository(BCP47Interface, BCP47Base):
    _BCP47_TYPE_PROCESSING_ORDER = [
        BCP47Type.SCRIPT, BCP47Type.LANGUAGE, BCP47Type.REGION, BCP47Type.VARIANT, BCP47Type.GRANDFATHERED,
        BCP47Type.REDUNDANT, BCP47Type.EXTLANG
    ]
    _BCP47_DEPENDENCY_FIELDS = [
        'macro_language',
        'preferred_value',
    ]
    _ITEM_SEPARATOR = '%%'
    _KEY_VALUE_SEPARATOR = ': '
    _FILE_HEADER = 'File-Date: '
    _VALUE_MAPPING: Dict[str, _BCP47ValueAttributes] = {
        'Type': _BCP47ValueAttributes(value_type=BCP47Type, internal_name='bcp_type'),
        'Subtag': _BCP47ValueAttributes(value_type=str, internal_name='subtag'),
        'Description': _BCP47ValueAttributes(value_type=list, internal_name='description'),
        'Suppress-Script': _BCP47ValueAttributes(value_type=str, internal_name='suppress_script'),
        'Scope': _BCP47ValueAttributes(value_type=str, internal_name='scope'),
        'Added': _BCP47ValueAttributes(value_type=datetime, internal_name='added'),
        'Macrolanguage': _BCP47ValueAttributes(value_type=str, internal_name='macro_language'),
        'Comments': _BCP47ValueAttributes(value_type=str, internal_name='comments'),
        'Preferred-Value': _BCP47ValueAttributes(value_type=str, internal_name='preferred_value'),
        'Deprecated': _BCP47ValueAttributes(value_type=datetime, internal_name='deprecated'),
        'Prefix': _BCP47ValueAttributes(value_type=list, internal_name='prefix'),
        'Tag': _BCP47ValueAttributes(value_type=str, internal_name='tag'),
    }
    _languages_scopes = (LanguageScopeEnum.COLLECTION, LanguageScopeEnum.PRIVATE_USE, LanguageScopeEnum.MACRO_LANGUAGE,
                         LanguageScopeEnum.SPECIAL)

    def __init__(self):
        super().__init__()
        self._SUBTAG_DATA_FINDER = [
            SubtagDataFinder(self.get_language_by_subtag, BCP47Type.LANGUAGE),
            SubtagDataFinder(self.get_ext_lang_by_subtag, BCP47Type.EXTLANG),
            SubtagDataFinder(self.get_script_by_subtag, BCP47Type.SCRIPT),
            SubtagDataFinder(self.get_region_by_subtag, BCP47Type.REGION),
            SubtagDataFinder(self.get_variant_by_subtag, BCP47Type.VARIANT)
        ]

        self._languages: List[BCP47Language] = []
        self._languages_scopes: List[BCP47LanguageScope] = []
        self._ext_langs: List[BCP47ExtLang] = []
        self._scripts: List[BCP47Script] = []
        self._regions: List[BCP47Region] = []
        self._variants: List[BCP47Variant] = []
        self._grandfathered: List[BCP47Grandfathered] = []
        self._redundant: List[BCP47Redundant] = []

        self._load_data()

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

    def _load_data(self):
        self._load_languages_scopes()
        self._load_bcp47()

    def _load_languages_scopes(self):
        for language_scope in LanguageScopeEnum:
            self._languages_scopes.append(BCP47LanguageScope(scope=language_scope))

    def _load_bcp47(self):
        with open(self._LANGUAGE_SUBTAG_REGISTRY_FILE_PATH, 'r', encoding='utf-8') as f:
            items = f.read().split(self._ITEM_SEPARATOR)

        updated_at = self._get_file_date(items.pop(0))
        data = [self._parse_item(item, updated_at) for item in items]
        del items
        data.sort(key=functools.cmp_to_key(self._sort_bcp47_items))

        for item in data:
            self._add_item(item)

    def _sort_bcp47_items(self, a: Dict[str, Any], b: Dict[str, Any]) -> int:
        if a['bcp_type'] != b['bcp_type']:
            a_index = self._BCP47_TYPE_PROCESSING_ORDER.index(a['bcp_type'])
            b_index = self._BCP47_TYPE_PROCESSING_ORDER.index(b['bcp_type'])
            return a_index - b_index

        if a.get('preferred_value') is not None and b.get('preferred_value') is None:
            return 1
        elif a.get('preferred_value') is None and b.get('preferred_value') is not None:
            return -1
        elif a.get('prefix') is not None and b.get('prefix') is None:
            return 1
        elif a.get('prefix') is None and b.get('prefix') is not None:
            return -1
        elif a.get('scope') is not None and b.get('scope') is None:
            return -1
        elif a.get('scope') is None and b.get('scope') is not None:
            return 1
        elif a.get('prefix') is not None and a.get('prefix') is not None:
            if a.get('prefix') > b.get('prefix'):
                return 1
            elif a.get('prefix') < b.get('prefix'):
                return -1
            return 0
        return 0

    def _get_file_date(self, text: str) -> datetime:
        if not text.startswith(self._FILE_HEADER):
            raise RuntimeError("Unexpected file format: File-Date not found")
        try:
            return datetime.fromisoformat(text[11:-1])
        except ValueError as e:
            raise RuntimeError("Unexpected file format: File-Date format is not valid") from e

    def _parse_item(self, item: str, updated_at: datetime) -> Dict[str, Any]:
        # TODO: Refactor
        data = {'updated_at': updated_at}
        previous_key: Optional[str] = None

        for value in item.strip().split("\n"):
            if value.startswith(' '):
                if not previous_key:
                    raise RuntimeError(f"There was no previous data to which it should be concatenated")
                previous_data_type = type(data[previous_key])
                if previous_data_type == list:
                    data[previous_key][-1] += value[1:]
                elif previous_data_type == str:
                    data[previous_key] += value[1:]
                else:
                    raise RuntimeError(f"Unexpected previous data type with a data that must be appended")

            else:
                key, value = value.split(self._KEY_VALUE_SEPARATOR, 1)
                if not (value_attributes := self._VALUE_MAPPING.get(key)):
                    raise RuntimeError(f"Unexpected BCP47 key: {key}")

                previous_key = value_attributes.internal_name

                if value_attributes.value_type == list:
                    if data.get(value_attributes.internal_name):
                        data[value_attributes.internal_name].append(value)
                    else:
                        data[value_attributes.internal_name] = [value]
                else:
                    if data.get(value_attributes.internal_name) is not None:
                        raise RuntimeError(f"Unexpected file format: Value key {key} is duplicated")

                    if value_attributes.value_type == datetime:
                        data[value_attributes.internal_name] = datetime.fromisoformat(value)
                    elif value_attributes.value_type == str:
                        data[value_attributes.internal_name] = value
                    elif value_attributes.value_type in (BCP47Type, LanguageScopeEnum):
                        try:
                            data[value_attributes.internal_name] = value_attributes.value_type(value)
                        except ValueError as e:
                            raise RuntimeError(f"Unexpected value type: {key}") from e
                    else:
                        raise RuntimeError(f"Value type {value_attributes.value_type} workflow is not properly "
                                           f"programmed")

        return data

    def _add_item(self, data_dict: Dict[str, Any]):
        try:
            bcp_type = data_dict.pop('bcp_type')
        except KeyError:
            raise RuntimeError(f"Unexpected workflow bcp_type was not retrieved")

        data_dict = self._replace_to_object(data_dict)

        if bcp_type == BCP47Type.LANGUAGE:
            self._load_language(data_dict)
        elif bcp_type == BCP47Type.EXTLANG:
            self._load_ext_lang(data_dict)
        elif bcp_type == BCP47Type.SCRIPT:
            self._load_script(data_dict)
        elif bcp_type == BCP47Type.REGION:
            self._load_region(data_dict)
        elif bcp_type == BCP47Type.VARIANT:
            self._load_variant(data_dict)
        elif bcp_type == BCP47Type.GRANDFATHERED:
            self._load_grandfathered(data_dict)
        elif bcp_type == BCP47Type.REDUNDANT:
            self._load_redundant(data_dict)
        else:
            raise RuntimeError(f"Unexpected workflow bcp_type unknown: {bcp_type}")

    def _load_language(self, data_dict: Dict[str, Any]):
        self._languages.append(BCP47Language(**data_dict))

    def _load_ext_lang(self, data_dict: Dict[str, Any]):
        self._ext_langs.append(BCP47ExtLang(**data_dict))

    def _load_script(self, data_dict: Dict[str, Any]):
        self._scripts.append(BCP47Script(**data_dict))

    def _load_region(self, data_dict: Dict[str, Any]):
        self._regions.append(BCP47Region(**data_dict))

    def _load_variant(self, data_dict: Dict[str, Any]):
        self._variants.append(BCP47Variant(**data_dict))

    def _load_grandfathered(self, data_dict: Dict[str, Any]):
        self._grandfathered.append(BCP47Grandfathered(**data_dict))

    def _load_redundant(self, data_dict: Dict[str, Any]):
        self._redundant.append(BCP47Redundant(**data_dict))

    def _replace_to_object(self, data_dict: Dict[str, Any]) -> Dict[str, Any]:
        if preferred_value := data_dict.pop('preferred_value', None):
            data_dict['preferred_value'] = self._tag_or_subtag_parser(preferred_value, case_sensitive=True)

        if suppress_script := data_dict.pop('suppress_script', None):
            data_dict['suppress_script'] = self.get_script_by_subtag(suppress_script, case_sensitive=True)

        if macro_language := data_dict.pop('macro_language', None):
            data_dict['macro_language'] = self.get_language_by_subtag(macro_language, case_sensitive=True)

        if langauge_scope := data_dict.pop('scope', None):
            data_dict['scope'] = self.get_language_scope_by_name(langauge_scope)

        if prefix_s := data_dict.pop('prefix', None):
            data_dict['prefix'] = self._parse_prefix(prefix_s, case_sensitive=True)

        return data_dict

    def _parse_to_object_preferred_value(self, bcp47_type: BCP47Type, data_dict: Dict[str, Any],
                                         preferred_value: str) -> Dict[str, Any]:
        if bcp47_type == BCP47Type.LANGUAGE:
            data_dict['preferred_value'] = self.get_language_by_subtag(preferred_value)
        elif bcp47_type == BCP47Type.EXTLANG:
            data_dict['preferred_value'] = self.get_ext_lang_by_subtag(preferred_value)
        elif bcp47_type == BCP47Type.SCRIPT:
            data_dict['preferred_value'] = self.get_script_by_subtag(preferred_value)
        elif bcp47_type == BCP47Type.REGION:
            data_dict['preferred_value'] = self.get_region_by_subtag(preferred_value)
        elif bcp47_type == BCP47Type.VARIANT:
            data_dict['preferred_value'] = self.get_variant_by_subtag(preferred_value)
        elif bcp47_type == BCP47Type.GRANDFATHERED:
            data_dict['preferred_value'] = self.get_grandfathered_by_tag(preferred_value)
        elif bcp47_type == BCP47Type.REDUNDANT:
            data_dict['preferred_value'] = self.get_redundant_by_tag(preferred_value)
        else:
            raise RuntimeError(f"Unexpected workflow bcp_type unknown: {bcp47_type}")
        return data_dict

    def _parse_prefix(
        self, prefix_list: List[str], case_sensitive: bool
    ) -> List[Dict[str, Union[BCP47Language, BCP47ExtLang, BCP47Script, BCP47Region, BCP47Variant, BCP47ExtLang]]]:
        prefix_f = []

        for prefix in prefix_list:
            prefix_f.append(self._tag_or_subtag_parser(prefix, case_sensitive))
        return prefix_f
