import operator
from typing import Callable, Any, Optional

from internationalization.models import Language, Region
from internationalization.models.language_scope import LanguageScope
from internationalization.models.script import Script
from internationalization.repositories.py_i18n_info.py_i18n_info_interface import \
    Pyi18nInfoInterface


class InternationalizationDataLoaderService:
    _PREFERRED_VALUE_OPERATOR_FUNC = (operator.not_, operator.truth)

    def load(self, py_i18n_info_repository: Pyi18nInfoInterface):
        self._load_scripts(py_i18n_info_repository)
        self._load_language_scopes(py_i18n_info_repository)
        self._load_languages(py_i18n_info_repository)
        self._load_regions(py_i18n_info_repository)

    def _load_scripts(self, py_i18n_info_repository: Pyi18nInfoInterface):
        for operator_func in self._PREFERRED_VALUE_OPERATOR_FUNC:
            self._load_scripts_batch(py_i18n_info_repository, operator_func)

    @staticmethod
    def _load_scripts_batch(py_i18n_info_repository: Pyi18nInfoInterface, operator_func: Callable[[Optional[Any]],
                                                                                                  bool]):
        scripts_iterator = (Script(
            source_data=script.source_data,
            updated_at=script.updated_at,
            added=script.added,
            deprecated=script.deprecated,
            description=script.description,
            subtag=script.subtag,
            comments=script.comments,
            preferred_value_script=script.preferred_value.script.id if script.preferred_value else None)
                            for script in py_i18n_info_repository.scripts if operator_func(script.preferred_value))

        Script.objects.bulk_create(scripts_iterator,
                                   update_conflicts=True,
                                   update_fields=[
                                       'source_data',
                                       'description',
                                       'added',
                                       'deprecated',
                                       'updated_at',
                                       'comments',
                                       'preferred_value_script',
                                   ],
                                   unique_fields=['subtag'])

        # If the model’s primary key is an AutoField, the primary key attribute can only be retrieved on certain
        #  databases (currently PostgreSQL, MariaDB 10.5+, and SQLite 3.35+). On other databases, it will not be set.
        #  https://docs.djangoproject.com/en/4.2/ref/models/querysets/#bulk-create
        for script_db in Script.objects.all():
            script = py_i18n_info_repository.get_script_by_subtag(script_db.subtag)
            script.id = script_db.id

    @staticmethod
    def _load_language_scopes(py_i18n_info_repository: Pyi18nInfoInterface):
        scopes = (LanguageScope(description=bcp47_language_scope.scope.value)
                  for bcp47_language_scope in py_i18n_info_repository.language_scopes)

        LanguageScope.objects.bulk_create(scopes, ignore_conflicts=True)
        # If the model’s primary key is an AutoField, the primary key attribute can only be retrieved on certain
        #  databases (currently PostgreSQL, MariaDB 10.5+, and SQLite 3.35+). On other databases, it will not be set.
        #  https://docs.djangoproject.com/en/4.2/ref/models/querysets/#bulk-create
        for language_scope_db in LanguageScope.objects.all():
            language_scope = py_i18n_info_repository.get_language_scope_by_name(language_scope_db.description)
            language_scope.id = language_scope_db.id

    def _load_languages(self, py_i18n_info_repository: Pyi18nInfoInterface):
        for operator_func in self._PREFERRED_VALUE_OPERATOR_FUNC:
            self._load_languages_batch(py_i18n_info_repository, operator_func)

    @staticmethod
    def _load_languages_batch(py_i18n_info_repository: Pyi18nInfoInterface, operator_func):
        languages = (Language(
            source_data=language.source_data,
            description=language.description,
            added=language.added,
            deprecated=language.deprecated,
            updated_at=language.updated_at,
            subtag=language.subtag,
            macro_language=language.macro_language.id if language.macro_language else None,
            scope=language.scope.id if language.scope else None,
            comments=language.comments,
            suppress_script=language.suppress_script.id if language.suppress_script else None,
            preferred_value_language=language.preferred_value.id if language.preferred_value else None,
            iso_639_1=language.iso_639_1,
            iso_639_2=language.iso_639_2,
            iso_639_3=language.iso_639_3,
            iso_639_5=language.iso_639_5,
        ) for language in py_i18n_info_repository.languages if operator_func(language.preferred_value))

        Language.objects.bulk_create(languages,
                                     update_conflicts=True,
                                     update_fields=[
                                         'source_data',
                                         'description',
                                         'added',
                                         'deprecated',
                                         'updated_at',
                                         'macro_language',
                                         'scope',
                                         'comments',
                                         'suppress_script',
                                         'preferred_value_language',
                                         'iso_639_1',
                                         'iso_639_2',
                                         'iso_639_3',
                                         'iso_639_5',
                                     ],
                                     unique_fields=['subtag'])

        # If the model’s primary key is an AutoField, the primary key attribute can only be retrieved on certain
        #  databases (currently PostgreSQL, MariaDB 10.5+, and SQLite 3.35+). On other databases, it will not be set.
        #  https://docs.djangoproject.com/en/4.2/ref/models/querysets/#bulk-create
        for language_db in Language.objects.all():
            language = py_i18n_info_repository.get_language_scope_by_name(language_db.description)
            language.id = language_db.id

    def _load_regions(self, py_i18n_info_repository: Pyi18nInfoInterface):
        regions_iterator = (Region() for region in py_i18n_info_repository.regions)
        Regions.obj

    #
    # def _load_regions(self):
    #     regions = [
    #         Region(deprecated_at=bcp47_region.deprecated,
    #                bcp47_region_subtag=bcp47_region.subtag,
    #                un_m49_code=bcp47_region.subtag if len(bcp47_region.subtag) == 3 else None,
    #                iso_3166_1_alpha_2_code=bcp47_region.subtag if len(bcp47_region.subtag) == 2 else None,
    #                iso_3166_1_alpha_3_code=None,
    #                comments=bcp47_region.comments,
    #                created_at=bcp47_region.added,
    #                updated_at=bcp47_region.updated_at,
    #                description=bcp47_region.description)
    #         for bcp47_region in self._internationalization_repository.regions if not bcp47_region.preferred_value
    #     ]
    #     Region.objects.bulk_create(regions,
    #                                update_conflicts=True,
    #                                update_fields=[
    #                                    'deprecated_at', 'bcp47_region_subtag', 'un_m49_code', 'iso_3166_1_alpha_2_code',
    #                                    'comments', 'created_at', 'updated_at', 'description'
    #                                ],
    #                                unique_fields=['bcp47_region_subtag'])
    #
    #     region_dict = {region.bcp47_region_subtag: region for region in Region.objects.all()}
    #     regions_replaced = [
    #         Region(
    #             preferred_value=region_dict[bcp47_region.preferred_value],
    #             deprecated_at=bcp47_region.deprecated,
    #             bcp47_region_subtag=bcp47_region.subtag,
    #             un_m49_code=bcp47_region.subtag if len(bcp47_region.subtag) == 3 else None,
    #             iso_3166_1_alpha_2_code=bcp47_region.subtag if len(bcp47_region.subtag) == 2 else None,
    #             iso_3166_1_alpha_3_code=None,
    #             comments=bcp47_region.comments,
    #             created_at=bcp47_region.added,
    #             updated_at=bcp47_region.updated_at,
    #             description='bcp47_region.description + [0]',
    #         ) for bcp47_region in self._internationalization_repository.regions if bcp47_region.preferred_value
    #     ]
    #     Region.objects.bulk_create(regions_replaced,
    #                                update_conflicts=True,
    #                                update_fields=[
    #                                    'deprecated_at', 'bcp47_region_subtag', 'un_m49_code', 'iso_3166_1_alpha_2_code',
    #                                    'comments', 'created_at', 'updated_at', 'description', 'preferred_value'
    #                                ],
    #                                unique_fields=['bcp47_region_subtag'])
