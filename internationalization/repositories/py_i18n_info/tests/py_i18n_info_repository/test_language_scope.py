import pytest

from internationalization.enums.language_scope import LanguageScopeEnum
from internationalization.repositories.py_i18n_info.exceptions.py_i18n_info_language_scope_not_found_error import \
    Pyi18nInfoLanguageScopeNotFoundError
from internationalization.repositories.py_i18n_info.py_i18n_info_interface import Pyi18nInfoInterface
from internationalization.repositories.py_i18n_info.schemas.py_i18n_info_language_scope import Pyi18nInfoLanguageScope


def test_py_i18n_info_repository_language_scope_list(py_i18n_info_repository_mock: Pyi18nInfoInterface):
    for language_scope in py_i18n_info_repository_mock.languages_scopes:
        assert type(language_scope) == Pyi18nInfoLanguageScope


def test_py_i18n_info_repository_language_scope_get_by_name(py_i18n_info_repository_mock: Pyi18nInfoInterface):
    assert py_i18n_info_repository_mock.get_language_scope_by_name('macrolanguage')


def test_py_i18n_info_repository_language_scope_get_by_name_not_found(
        py_i18n_info_repository_mock: Pyi18nInfoInterface):
    with pytest.raises(Pyi18nInfoLanguageScopeNotFoundError):
        assert py_i18n_info_repository_mock.get_language_scope_by_name('err')


def test_py_i18n_info_repository_language_scope_id(py_i18n_info_repository_mock: Pyi18nInfoInterface):
    for language_scope in py_i18n_info_repository_mock.languages_scopes:
        assert language_scope.id is None


def test_py_i18n_info_repository_language_i18n_info(py_i18n_info_repository_mock: Pyi18nInfoInterface):
    for language_scope in py_i18n_info_repository_mock.languages_scopes:
        assert language_scope.i18n_info == {}  # FIXME: in some moment it should be populated


def test_py_i18n_info_repository_language_scope_scope(py_i18n_info_repository_mock: Pyi18nInfoInterface):
    macro_language = py_i18n_info_repository_mock.get_language_scope_by_name('macrolanguage')
    assert macro_language.scope == LanguageScopeEnum.MACRO_LANGUAGE
