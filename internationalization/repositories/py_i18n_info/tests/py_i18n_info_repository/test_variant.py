import pytest

from internationalization.repositories.py_i18n_info.exceptions.py_i18n_info_variant_subtag_not_found_error import \
    Pyi18nInfoVariantSubtagNotFoundError
from internationalization.repositories.py_i18n_info.py_i18n_info_interface import Pyi18nInfoInterface
from internationalization.repositories.py_i18n_info.schemas.py_i18n_info_variant import Pyi18nInfoVariant


def test_py_i18n_info_repository_variant_list(py_i18n_info_repository_mock: Pyi18nInfoInterface):
    assert py_i18n_info_repository_mock.variants

    for variant in py_i18n_info_repository_mock.variants:
        assert isinstance(variant, Pyi18nInfoVariant)


def test_py_i18n_info_repository_variant_get_by_subtag_case_insensitive(
        py_i18n_info_repository_mock: Pyi18nInfoInterface):
    latin = py_i18n_info_repository_mock.get_variant_by_subtag('latn', case_sensitive=False)
    assert latin.subtag == 'Latn'

    latin = py_i18n_info_repository_mock.get_variant_by_subtag('Latn', case_sensitive=False)
    assert latin.subtag == 'Latn'


def test_py_i18n_info_repository_variant_get_by_subtag_not_found(py_i18n_info_repository_mock: Pyi18nInfoInterface):
    with pytest.raises(Pyi18nInfoVariantSubtagNotFoundError):
        py_i18n_info_repository_mock.get_variant_by_subtag('Err')


def test_py_i18n_info_repository_variant_get_by_subtag_case_sensitive(py_i18n_info_repository_mock: Pyi18nInfoInterface):
    with pytest.raises(Pyi18nInfoVariantSubtagNotFoundError):
        py_i18n_info_repository_mock.get_variant_by_subtag('latn', case_sensitive=True)

    latin = py_i18n_info_repository_mock.get_variant_by_subtag('Latn', case_sensitive=True)
    assert latin.subtag == 'Latn'


def test_py_i18n_info_repository_variant_id(py_i18n_info_repository_mock: Pyi18nInfoInterface):
    for variant in py_i18n_info_repository_mock.variants:
        assert variant.id is None