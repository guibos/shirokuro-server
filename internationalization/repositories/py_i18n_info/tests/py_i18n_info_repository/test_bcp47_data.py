import pytest

from internationalization.repositories.bcp47.bcp47_repository import BCP47Repository
from internationalization.repositories.py_i18n_info.py_i18n_info_interface import Pyi18nInfoInterface
from internationalization.repositories.py_i18n_info.py_i18n_info_repository import Pyi18nInfoRepository
from internationalization.repositories.py_i18n_info.schemas.py_i18n_info_ext_lang import Pyi18nInfoExtLang
from internationalization.repositories.py_i18n_info.schemas.py_i18n_info_grandfathered import Pyi18nInfoGrandfathered
from internationalization.repositories.py_i18n_info.schemas.py_i18n_info_language import Pyi18nInfoLanguage
from internationalization.repositories.py_i18n_info.schemas.py_i18n_info_language_scope import Pyi18nInfoLanguageScope
from internationalization.repositories.py_i18n_info.schemas.py_i18n_info_redundant import Pyi18nInfoRedundant
from internationalization.repositories.py_i18n_info.schemas.py_i18n_info_region import Pyi18nInfoRegion
from internationalization.repositories.py_i18n_info.schemas.py_i18n_info_script import Pyi18nInfoScript


@pytest.fixture(scope="module")
def py_i18n_info_repo():
    return Pyi18nInfoRepository(BCP47Repository())


@pytest.mark.non_mocked
def test_py_i18n_info_repository_bcp47_data_scripts(py_i18n_info_repo: Pyi18nInfoInterface):
    assert py_i18n_info_repo.scripts

    for script in py_i18n_info_repo.scripts:
        assert isinstance(script, Pyi18nInfoScript)


@pytest.mark.non_mocked
def test_py_i18n_info_repository_bcp47_data_regions(py_i18n_info_repo: Pyi18nInfoInterface):
    assert py_i18n_info_repo.regions

    for region in py_i18n_info_repo.regions:
        assert isinstance(region, Pyi18nInfoRegion)


@pytest.mark.non_mocked
def test_py_i18n_info_repository_bcp47_data_languages(py_i18n_info_repo: Pyi18nInfoInterface):
    assert py_i18n_info_repo.languages

    for language in py_i18n_info_repo.regions:
        assert isinstance(language, Pyi18nInfoLanguage)


@pytest.mark.non_mocked
def test_py_i18n_info_repository_bcp47_data_ext_langs(py_i18n_info_repo: Pyi18nInfoInterface):
    assert py_i18n_info_repo.ext_langs

    for ext_lang in py_i18n_info_repo.ext_langs:
        assert isinstance(ext_lang, Pyi18nInfoExtLang)


@pytest.mark.non_mocked
def test_py_i18n_info_repository_bcp47_data_grandfathered(py_i18n_info_repo: Pyi18nInfoInterface):
    assert py_i18n_info_repo.grandfathered

    for grandfathered in py_i18n_info_repo.grandfathered:
        assert isinstance(grandfathered, Pyi18nInfoGrandfathered)


@pytest.mark.non_mocked
def test_py_i18n_info_repository_bcp47_data_language_scope(py_i18n_info_repo: Pyi18nInfoInterface):
    assert py_i18n_info_repo.languages_scopes

    for language_scope in py_i18n_info_repo.languages_scopes:
        assert isinstance(language_scope, Pyi18nInfoLanguageScope)


@pytest.mark.non_mocked
def test_py_i18n_info_repository_bcp47_data_redundant(py_i18n_info_repo: Pyi18nInfoInterface):
    assert py_i18n_info_repo.redundant

    for redundant in py_i18n_info_repo.redundant:
        assert isinstance(redundant, Pyi18nInfoRedundant)


@pytest.mark.non_mocked
def test_py_i18n_info_repository_bcp47_data_variants(py_i18n_info_repo: Pyi18nInfoInterface):
    assert py_i18n_info_repo.variants

    for variant in py_i18n_info_repo.variants:
        assert isinstance(variant, Pyi18nInfoRedundant)
