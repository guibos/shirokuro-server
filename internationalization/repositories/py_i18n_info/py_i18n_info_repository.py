import dataclasses
import logging
import os.path
from collections import defaultdict
from typing import List, Optional, Dict, Union, Callable

import rdflib
from pydantic import AnyUrl
from pydantic_core import Url
from rdflib import URIRef, BNode

from internationalization.enums.bcp47_type import BCP47Type
from internationalization.repositories.bcp47.bcp47_interface import BCP47Interface
from internationalization.repositories.bcp47.exceptions.language_subtag_not_found_error import \
    LanguageSubtagNotFoundError
from internationalization.repositories.bcp47.exceptions.tag_or_subtag_not_found_error import TagOrSubtagNotFoundError
from internationalization.repositories.bcp47.schemas.abstract.subtag_data_finder import SubtagDataFinder
from internationalization.repositories.bcp47.schemas.bcp47_ext_lang import BCP47ExtLang
from internationalization.repositories.bcp47.schemas.bcp47_grandfathered import BCP47Grandfathered
from internationalization.repositories.bcp47.schemas.bcp47_language import BCP47Language
from internationalization.repositories.bcp47.schemas.bcp47_redundant import BCP47Redundant
from internationalization.repositories.bcp47.schemas.bcp47_region import BCP47Region
from internationalization.repositories.bcp47.schemas.bcp47_script import BCP47Script
from internationalization.repositories.bcp47.schemas.bcp47_variant import BCP47Variant
from internationalization.repositories.bcp47.type_aliases import BCP47PrefixesType, BCP47PreferredValuesType
from internationalization.repositories.py_i18n_info._py_i18n_info_base import Pyi18nInfoBase
from internationalization.repositories.py_i18n_info.py_i18n_info_interface import \
    Pyi18nInfoInterface
from internationalization.repositories.py_i18n_info.schemas.abstract.py_i18n_info_translation import \
    Pyi18nInfoTranslation
from internationalization.repositories.py_i18n_info.schemas.py_i18n_info_ext_lang import Pyi18nInfoExtLang, \
    Pyi18nInfoExtLangPreferredValue, Pyi18nInfoExtLangPrefix
from internationalization.repositories.py_i18n_info.schemas.py_i18n_info_grandfathered import \
    Pyi18nInfoGrandfathered, Pyi18nInfoGrandfatheredPreferredValue, Pyi18nInfoGrandfatheredPrefix
from internationalization.repositories.py_i18n_info.schemas.py_i18n_info_language import Pyi18nInfoLanguage, \
    Pyi18nInfoLanguagePreferredValue
from internationalization.repositories.py_i18n_info.schemas.py_i18n_info_language_scope import Pyi18nInfoLanguageScope
from internationalization.repositories.py_i18n_info.schemas.py_i18n_info_redundant import Pyi18nInfoRedundant, \
    Pyi18nInfoRedundantPreferredValue
from internationalization.repositories.py_i18n_info.schemas.py_i18n_info_region import Pyi18nInfoRegion, \
    Pyi18nInfoRegionPreferredValue
from internationalization.repositories.py_i18n_info.schemas.py_i18n_info_script import Pyi18nInfoScript
from internationalization.repositories.py_i18n_info.schemas.py_i18n_info_subtags import Pyi18nInfoSubtags
from internationalization.repositories.py_i18n_info.schemas.py_i18n_info_variant import Pyi18nInfoVariant, \
    Pyi18nInfoVariantPreferredValue, Pyi18nInfoVariantPrefix
from internationalization.repositories.py_i18n_info.type_aliases import SubtagsType, TagsOrSubtags


@dataclasses.dataclass
class SemanticDownloadConfig:
    path: str
    uri_ref: URIRef


@dataclasses.dataclass
class _I18nLoaderInfo:
    data: List[TagsOrSubtags]
    bcp_47_type: BCP47Type
    semantic_data_dir: str


class Pyi18nInfoRepository(Pyi18nInfoInterface, Pyi18nInfoBase):
    _PREDICATE_ISO_639_1 = rdflib.term.URIRef('http://www.wikidata.org/prop/direct/P218')
    _PREDICATE_ISO_639_2 = rdflib.term.URIRef('http://www.wikidata.org/prop/direct/P219')
    _PREDICATE_ISO_639_3 = rdflib.term.URIRef('http://www.wikidata.org/prop/direct/P220')
    _PREDICATE_ISO_639_5 = rdflib.term.URIRef('http://www.wikidata.org/prop/direct/P1798')
    _PREDICATE_ISO_639_6 = rdflib.term.URIRef('http://www.wikidata.org/prop/direct/P221')
    _PREDICATE_ISO_3166_1_ALPHA_2 = rdflib.term.URIRef('http://www.wikidata.org/prop/direct/P297')
    _PREDICATE_ISO_3166_1_ALPHA_3 = rdflib.term.URIRef('http://www.wikidata.org/prop/direct/P298')
    _PREDICATE_ISO_3166_1_NUM = rdflib.term.URIRef('http://www.wikidata.org/prop/direct/P299')
    _PREDICATE_OFFICIAL_LANGUAGE = rdflib.term.URIRef('http://www.wikidata.org/prop/direct/P37')
    _PREDICATE_LANGUAGE_USED = rdflib.term.URIRef('http://www.wikidata.org/prop/direct/P2936')
    _PREDICATE_DESCRIPTION = rdflib.term.URIRef('http://schema.org/description')
    _PREDICATE_PREFERRED_LABEL = rdflib.term.URIRef('http://www.w3.org/2004/02/skos/core#prefLabel')

    def __init__(self, bcp47_repository: BCP47Interface):
        super().__init__()
        self._TAG_OR_SUBTAG_DATA_FINDER = [
            SubtagDataFinder(self.get_language_by_subtag, BCP47Type.LANGUAGE),
            SubtagDataFinder(self.get_ext_lang_by_subtag, BCP47Type.EXTLANG),
            SubtagDataFinder(self.get_script_by_subtag, BCP47Type.SCRIPT),
            SubtagDataFinder(self.get_region_by_subtag, BCP47Type.REGION),
            SubtagDataFinder(self.get_variant_by_subtag, BCP47Type.VARIANT)
        ]
        self._MAPPING_GETTER_WITH_KEY = {
            'language': self.get_language_by_subtag,
            'extlang': self.get_ext_lang_by_subtag,
            'script': self.get_script_by_subtag,
            'region': self.get_region_by_subtag,
            'variant': self.get_variant_by_subtag,
            'grandfathered': self.get_grandfathered_by_tag,
            'redundant': self.get_redundant_by_tag
        }

        self._languages: List[Pyi18nInfoLanguage] = []
        self._languages_scopes: List[Pyi18nInfoLanguageScope] = []
        self._ext_langs: List[Pyi18nInfoExtLang] = []
        self._scripts: List[Pyi18nInfoScript] = []
        self._regions: List[Pyi18nInfoRegion] = []
        self._variants: List[Pyi18nInfoVariant] = []
        self._grandfathered: List[Pyi18nInfoGrandfathered] = []
        self._redundant: List[Pyi18nInfoRedundant] = []

        self._load_data(bcp47_repository)

    @property
    def languages_scopes(self):
        return self._languages_scopes

    @property
    def languages(self) -> List[Pyi18nInfoLanguage]:
        return self._languages

    def get_language_by_source_data(self, uri: str) -> Pyi18nInfoLanguage:
        try:
            return self._source_data_filter(uri, self.languages)
        except TagOrSubtagNotFoundError as e:
            raise LanguageSubtagNotFoundError(uri) from e

    @property
    def ext_langs(self) -> List[Pyi18nInfoExtLang]:
        return self._ext_langs

    @property
    def scripts(self) -> List[Pyi18nInfoScript]:
        return self._scripts

    @property
    def regions(self) -> List[Pyi18nInfoRegion]:
        return self._regions

    @property
    def variants(self) -> List[Pyi18nInfoVariant]:
        return self._variants

    @property
    def grandfathered(self) -> List[Pyi18nInfoGrandfathered]:
        return self._grandfathered

    @property
    def redundant(self) -> List[Pyi18nInfoRedundant]:
        return self._redundant

    @staticmethod
    def _source_data_filter(source_data: str, subtag_list: List[SubtagsType]) -> SubtagsType:
        source_data = Url(source_data)

        for subtag in subtag_list:
            if source_data == subtag.source_data:
                return subtag
        raise TagOrSubtagNotFoundError(source_data)

    def _load_data(self, bcp47_repository: BCP47Interface):
        self._load_scripts(bcp47_repository)
        self._load_language_scopes(bcp47_repository)
        self._load_languages(bcp47_repository)
        self._load_extlang(bcp47_repository)
        self._load_regions(bcp47_repository)
        self._load_variants(bcp47_repository)
        self._load_grandfather(bcp47_repository)
        self._load_redundant(bcp47_repository)

        parse_data = [
            _I18nLoaderInfo(self.scripts, BCP47Type.SCRIPT, self._SEMANTIC_SCRIPT_DATA_DIR),
            _I18nLoaderInfo(self.languages, BCP47Type.LANGUAGE, self._SEMANTIC_LANGUAGE_DATA_DIR),
            _I18nLoaderInfo(self.regions, BCP47Type.REGION, self._SEMANTIC_REGION_DATA_DIR),
            _I18nLoaderInfo(self.ext_langs, BCP47Type.EXTLANG, self._SEMANTIC_LANGUAGE_DATA_DIR),
            _I18nLoaderInfo(self.variants, BCP47Type.VARIANT, self._SEMANTIC_VARIANT_DATA_DIR),
            _I18nLoaderInfo(self.grandfathered, BCP47Type.GRANDFATHERED, self._SEMANTIC_GRANDFATHERED_DATA_DIR),
            _I18nLoaderInfo(self.redundant, BCP47Type.REDUNDANT, self._SEMANTIC_REDUNDANT_DATA_DIR)
        ]
        for i18n_loader_info in parse_data:
            for tag_or_subtag in i18n_loader_info.data:
                tag_or_subtag_str = self._get_tag_or_subtag(tag_or_subtag)
                tag_or_subtag.i18n_info = self._get_i18n_data(i18n_loader_info.bcp_47_type, tag_or_subtag_str,
                                                              tag_or_subtag.source_data,
                                                              i18n_loader_info.semantic_data_dir)

    def _load_scripts(self, bcp47_repository: BCP47Interface):
        for script in bcp47_repository.scripts:
            self._scripts.append(self._bcp47_script_to_py18n_info(script))

    def _bcp47_script_to_py18n_info(self, script: BCP47Script) -> Pyi18nInfoScript:
        graph = self._get_graph(BCP47Type.SCRIPT, script.subtag, data_dir=self._SEMANTIC_SCRIPT_DATA_DIR)

        tri_object: rdflib.term.Literal
        source_data: Optional[str] = None

        if graph:
            source_data = str(next(graph.triples((None, URIRef(self._PREDICATE_PREFERRED_LABEL), None)))[0])
        else:
            logging.warning('Not i18n information found for script subtag: "%s"', script.subtag)

        return Pyi18nInfoScript(source_data=source_data,
                                i18n_info={},
                                comments=script.comments,
                                subtag=script.subtag,
                                description=script.description,
                                added=script.added,
                                deprecated=script.deprecated,
                                updated_at=script.updated_at)

    def _load_language_scopes(self, bcp47_repository: BCP47Interface):
        for language_scope in bcp47_repository.languages_scopes:
            language_scope_i18n = Pyi18nInfoLanguageScope(scope=language_scope.scope)
            self._languages_scopes.append(language_scope_i18n)

    def _load_languages(self, bcp47_repository: BCP47Interface):
        for language in bcp47_repository.languages:
            self._languages.append(self._bcp47_language_to_py18n_info(language))

    def _bcp47_language_to_py18n_info(self, language: BCP47Language) -> Pyi18nInfoLanguage:
        graph = self._get_graph(BCP47Type.LANGUAGE, language.subtag, data_dir=self._SEMANTIC_LANGUAGE_DATA_DIR)

        iso_639_1: Optional[str] = None
        iso_639_2: Optional[str] = None
        iso_639_3: Optional[str] = None
        iso_639_5: Optional[str] = None
        tri_object: rdflib.term.Literal
        macro_language = self.get_language_by_subtag(
            language.macro_language.subtag) if language.macro_language else None
        suppress_script = self.get_script_by_subtag(
            language.suppress_script.subtag) if language.suppress_script else None
        preferred_value = None
        scope = self.get_language_scope_by_name(language.scope.scope.value) if language.scope else None

        if language.preferred_value:
            data_dict = self._transform_bcp47_tags_to_py_i18n_info(language.preferred_value)
            preferred_value = Pyi18nInfoLanguagePreferredValue(**data_dict)
        source_data: Optional[str] = None

        if graph:
            source_data = str(next(graph.triples((None, URIRef(self._PREDICATE_PREFERRED_LABEL), None)))[0])
            for (subject, predicate, tri_object) in graph.triples((None, None, None)):
                if type(tri_object) == BNode:
                    continue
                if predicate == self._PREDICATE_ISO_639_1:
                    iso_639_1 = tri_object.value
                elif predicate == self._PREDICATE_ISO_639_2:
                    iso_639_2 = tri_object.value
                elif predicate == self._PREDICATE_ISO_639_3:
                    iso_639_3 = tri_object.value
                elif predicate == self._PREDICATE_ISO_639_5:
                    iso_639_5 = tri_object.value
        else:
            logging.warning('Not i18n information found for language subtag: "%s"', language.subtag)

        return Pyi18nInfoLanguage(
            subtag=language.subtag,
            i18n_info={},
            description=language.description,
            added=language.added,
            deprecated=language.deprecated,
            updated_at=language.updated_at,
            macro_language=macro_language,
            scope=scope,
            comments=language.comments,
            suppress_script=suppress_script,
            preferred_value=preferred_value,
            source_data=source_data,
            iso_639_1=iso_639_1,
            iso_639_2=iso_639_2,
            iso_639_3=iso_639_3,
            iso_639_5=iso_639_5,
        )

    def _load_extlang(self, bcp47_repository: BCP47Interface):
        for ext_lang in bcp47_repository.ext_langs:
            self._ext_langs.append(self._bcp47_extlang_to_py18n_info(ext_lang))

    def _bcp47_extlang_to_py18n_info(self, ext_lang: BCP47ExtLang) -> Pyi18nInfoExtLang:
        graph = self._get_graph(BCP47Type.REGION, ext_lang.subtag, data_dir=self._SEMANTIC_LANGUAGE_DATA_DIR)

        tri_object: rdflib.term.Literal
        preferred_value = None
        prefixes = []
        if ext_lang.preferred_value:
            data_dict = self._transform_bcp47_tags_to_py_i18n_info(ext_lang.preferred_value)
            preferred_value = Pyi18nInfoExtLangPreferredValue(**data_dict)

        for prefix in ext_lang.prefix:
            data_dict = self._transform_bcp47_tags_to_py_i18n_info(prefix)
            prefixes.append(Pyi18nInfoExtLangPrefix(**data_dict))

        source_data: Optional[str] = None
        macro_language = self.get_language_by_subtag(
            ext_lang.macro_language.subtag) if ext_lang.macro_language else None

        if graph:
            source_data = str(next(graph.triples((None, URIRef(self._PREDICATE_PREFERRED_LABEL), None)))[0])
        else:
            logging.warning('Not i18n information found for extlang subtag: "%s"', ext_lang.subtag)

        return Pyi18nInfoExtLang(
            subtag=ext_lang.subtag,
            description=ext_lang.description,
            added=ext_lang.added,
            deprecated=ext_lang.deprecated,
            updated_at=ext_lang.updated_at,
            source_data=source_data,
            i18n_info={},
            prefix=prefixes,
            macro_language=macro_language,
            preferred_value=preferred_value,
        )

    def _load_regions(self, bcp47_repository: BCP47Interface):
        for region in bcp47_repository.regions:
            self._regions.append(self._bcp47_region_to_py18n_info(region))

    def _bcp47_region_to_py18n_info(self, region: BCP47Region) -> Pyi18nInfoRegion:
        graph = self._get_graph(BCP47Type.REGION, region.subtag, data_dir=self._SEMANTIC_REGION_DATA_DIR)

        tri_object: rdflib.term.Literal
        preferred_value = None
        if region.preferred_value:
            data_dict = self._transform_bcp47_tags_to_py_i18n_info(region.preferred_value)
            preferred_value = Pyi18nInfoRegionPreferredValue(**data_dict)
        source_data: Optional[str] = None
        iso3166_1_alpha2: Optional[str] = None
        iso3166_1_alpha3: Optional[str] = None
        iso3166_1_numeric: Optional[str] = None
        official_languages: List[Pyi18nInfoLanguage] = []
        used_languages: List[Pyi18nInfoLanguage] = []

        if graph:
            source_data = str(next(graph.triples((None, URIRef(self._PREDICATE_PREFERRED_LABEL), None)))[0])
            for (subject, predicate, tri_object) in graph.triples((None, None, None)):
                if type(tri_object) == BNode:
                    continue
                if predicate == self._PREDICATE_ISO_3166_1_ALPHA_2:
                    iso3166_1_alpha2 = tri_object.value
                elif predicate == self._PREDICATE_ISO_3166_1_ALPHA_3:
                    iso3166_1_alpha3 = tri_object.value
                elif predicate == self._PREDICATE_ISO_3166_1_NUM:
                    iso3166_1_numeric = tri_object.value
                elif predicate == self._PREDICATE_OFFICIAL_LANGUAGE:
                    try:
                        official_languages.append(self.get_language_by_source_data(tri_object))
                    except LanguageSubtagNotFoundError:
                        logging.warning('Language data_source "%": not found.')
                elif predicate == self._PREDICATE_LANGUAGE_USED:
                    try:
                        used_languages.append(self.get_language_by_source_data(tri_object))
                    except LanguageSubtagNotFoundError:
                        logging.warning('Language data_source "%": not found.')

        else:
            logging.warning('Not i18n information found for region subtag: "%s"', region.subtag)

        return Pyi18nInfoRegion(source_data=source_data,
                                i18n_info={},
                                iso3166_1_alpha2=iso3166_1_alpha2,
                                iso3166_1_alpha3=iso3166_1_alpha3,
                                iso3166_1_numeric=iso3166_1_numeric,
                                comments=region.comments,
                                preferred_value=preferred_value,
                                subtag=region.subtag,
                                description=region.description,
                                added=region.added,
                                deprecated=region.deprecated,
                                updated_at=region.updated_at,
                                official_languages=official_languages,
                                used_languages=used_languages)

    def _load_variants(self, bcp47_repository: BCP47Interface):
        for variant in bcp47_repository.variants:
            self._variants.append(self._bcp47_variant_to_py18n_info(variant))

    def _bcp47_variant_to_py18n_info(self, variant: BCP47Variant) -> Pyi18nInfoVariant:
        graph = self._get_graph(BCP47Type.VARIANT, variant.subtag, data_dir=self._SEMANTIC_VARIANT_DATA_DIR)

        tri_object: rdflib.term.Literal
        prefixes = []
        preferred_value = None
        iso_639_6: Optional[str] = None

        if variant.preferred_value:
            data_dict = self._transform_bcp47_tags_to_py_i18n_info(variant.preferred_value)
            preferred_value = Pyi18nInfoVariantPreferredValue(**data_dict)

        for prefix in variant.prefix:
            data_dict = self._transform_bcp47_tags_to_py_i18n_info(prefix)
            prefixes.append(Pyi18nInfoVariantPrefix(**data_dict))
        source_data: Optional[str] = None

        if graph:
            source_data = str(next(graph.triples((None, URIRef(self._PREDICATE_PREFERRED_LABEL), None)))[0])
            for (subject, predicate, tri_object) in graph.triples((None, None, None)):
                if type(tri_object) == BNode:
                    continue
                elif predicate == self._PREDICATE_ISO_639_6:
                    iso_639_6 = tri_object.value

        else:
            logging.warning('Not i18n information found for variant subtag: "%s"', variant.subtag)

        return Pyi18nInfoVariant(source_data=source_data,
                                 i18n_info={},
                                 comments=variant.comments,
                                 preferred_value=preferred_value,
                                 subtag=variant.subtag,
                                 description=variant.description,
                                 added=variant.added,
                                 deprecated=variant.deprecated,
                                 updated_at=variant.updated_at,
                                 prefix=prefixes,
                                 iso_639_6=iso_639_6)

    def _load_grandfather(self, bcp47_repository: BCP47Interface):
        for grandfathered in bcp47_repository.grandfathered:
            self._grandfathered.append(self._bcp47_grandfathered_to_py18n_info(grandfathered))

    def _bcp47_grandfathered_to_py18n_info(self, grandfathered: BCP47Grandfathered) -> Pyi18nInfoGrandfathered:
        graph = self._get_graph(BCP47Type.GRANDFATHERED,
                                grandfathered.tag,
                                data_dir=self._SEMANTIC_GRANDFATHERED_DATA_DIR)

        tri_object: rdflib.term.Literal
        prefixes = []
        preferred_value = None
        if grandfathered.preferred_value:
            data_dict = self._transform_bcp47_tags_to_py_i18n_info(grandfathered.preferred_value)
            preferred_value = Pyi18nInfoGrandfatheredPreferredValue(**data_dict)

        for prefix in grandfathered.prefix:
            data_dict = self._transform_bcp47_tags_to_py_i18n_info(prefix)
            prefixes.append(Pyi18nInfoGrandfatheredPrefix(**data_dict))
        source_data: Optional[str] = None

        if graph:
            source_data = str(next(graph.triples((None, URIRef(self._PREDICATE_PREFERRED_LABEL), None)))[0])
        else:
            logging.warning('Not i18n information found for grandfathered tag: "%s"', grandfathered.tag)

        return Pyi18nInfoGrandfathered(source_data=source_data,
                                       i18n_info={},
                                       comments=grandfathered.comments,
                                       preferred_value=preferred_value,
                                       tag=grandfathered.tag,
                                       description=grandfathered.description,
                                       added=grandfathered.added,
                                       deprecated=grandfathered.deprecated,
                                       updated_at=grandfathered.updated_at,
                                       prefix=prefixes)

    def _load_redundant(self, bcp47_repository: BCP47Interface):
        for redundant in bcp47_repository.redundant:
            self._redundant.append(self._bcp47_redundant_to_py18n_info(redundant))

    def _bcp47_redundant_to_py18n_info(self, redundant: BCP47Redundant) -> Pyi18nInfoRedundant:
        graph = self._get_graph(BCP47Type.REDUNDANT, redundant.tag, data_dir=self._SEMANTIC_REDUNDANT_DATA_DIR)

        tri_object: rdflib.term.Literal
        preferred_value = None
        if redundant.preferred_value:
            data_dict = self._transform_bcp47_tags_to_py_i18n_info(redundant.preferred_value)
            preferred_value = Pyi18nInfoRedundantPreferredValue(**data_dict)
        source_data: Optional[str] = None

        if graph:
            source_data = str(next(graph.triples((None, URIRef(self._PREDICATE_PREFERRED_LABEL), None)))[0])
        else:
            logging.warning('Not i18n information found for grandfathered tag: "%s"', redundant.tag)

        return Pyi18nInfoRedundant(
            source_data=source_data,
            i18n_info={},
            preferred_value=preferred_value,
            tag=redundant.tag,
            description=redundant.description,
            added=redundant.added,
            deprecated=redundant.deprecated,
            updated_at=redundant.updated_at,
        )

    def _transform_bcp47_tags_to_py_i18n_info(
            self, model: Union[BCP47PreferredValuesType, BCP47PrefixesType]) -> Dict[str, TagsOrSubtags]:
        value_dict = {}
        for attribute_name in model.model_fields_set:
            attribute: TagsOrSubtags = getattr(model, attribute_name)
            if attribute:
                func: Callable[[str], TagsOrSubtags] = self._MAPPING_GETTER_WITH_KEY[attribute_name]
                value_dict[attribute_name] = func(self._get_tag_or_subtag(attribute))
        return value_dict

    @staticmethod
    def _get_tag_or_subtag(model: TagsOrSubtags) -> str:
        if str_tag_or_subtag := getattr(model, 'subtag', ''):
            return str_tag_or_subtag
        elif str_tag_or_subtag := getattr(model, 'tag', ''):
            return str_tag_or_subtag
        raise RuntimeError("Tag or subtag not found.")

    def _get_i18n_data(self, bcp47_type: BCP47Type, tag_or_subtag: str, source_data: AnyUrl,
                       semantic_data_dir: str) -> Dict[Pyi18nInfoSubtags, Pyi18nInfoTranslation]:
        graph = self._get_graph(bcp47_type, tag_or_subtag, data_dir=semantic_data_dir)
        i18n_info = {}
        i18n_info_dict = defaultdict(dict)

        if not graph:
            return {}

        for subject, predicate, tri_object in graph.triples((None, None, None)):
            if predicate == self._PREDICATE_PREFERRED_LABEL:
                try:
                    internationalization_tag_or_subtag = self.tag_or_subtag_parser(tri_object.language)
                except TagOrSubtagNotFoundError:
                    logging.exception("Not possible to load a internationalization due a previous error.")
                    continue
                i18n_info_dict[internationalization_tag_or_subtag]['name'] = tri_object.value
            elif predicate == self._PREDICATE_DESCRIPTION:
                try:
                    internationalization_tag_or_subtag = self.tag_or_subtag_parser(tri_object.language)
                except TagOrSubtagNotFoundError:
                    logging.exception("Not possible to load a internationalization due a previous error.")
                    continue
                i18n_info_dict[internationalization_tag_or_subtag]['description'] = tri_object.value

        for key, value in i18n_info_dict.items():
            if value.get('description') and not value.get('name'):
                logging.warning(
                    'Tag or subtag "%s" have internationalization with tag or subtag '
                    '"%s" for description but not for name. '
                    'Name is a mandatory field for the model. This internationalization will not be used. '
                    'You could add internationalization name in: %s', tag_or_subtag, key.tag, source_data)
            else:
                i18n_info[key] = Pyi18nInfoTranslation(**value)
        return i18n_info

    def _get_graph(self, subtag_type: BCP47Type, subtag: str, data_dir: str) -> Optional[rdflib.Graph]:
        path = os.path.join(data_dir, self._SEMANTIC_PREFIX_FILE + subtag + self._SEMANTIC_EXTENSION_FILE)
        graph = rdflib.Graph()
        if not os.path.isfile(path):
            logging.info("%s subtag with value: %s was not found.", subtag_type.value, subtag)
            return
        return graph.parse(path)
