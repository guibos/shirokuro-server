from datetime import datetime

import pytest
from pydantic_core import Url

from internationalization.repositories.bcp47.bcp47_interface import BCP47Interface
from internationalization.repositories.py_i18n_info.py_i18n_info_interface import Pyi18nInfoInterface
from internationalization.repositories.py_i18n_info.py_i18n_info_repository import Pyi18nInfoRepository


@pytest.fixture(scope="session")
def py_i18n_info_repository_mock(bcp47_mock: BCP47Interface) -> Pyi18nInfoInterface:
    return Pyi18nInfoRepository(bcp47_mock)


def _check_script(py_i18n_info_repository: Pyi18nInfoInterface):
    latin = py_i18n_info_repository.get_script_by_subtag('Latn')

    assert latin.id is None
    assert latin.source_data == Url('http://www.wikidata.org/entity/Q8229')
    assert latin.i18n_info == {}
    assert latin.description == ['Latin']
    assert latin.added == datetime(2005, 10, 16, 0, 0)
    assert latin.deprecated is None
    assert type(latin.updated_at) == datetime
    assert latin.subtag == 'Latn'
    assert latin.comments is None


def test_py_i18n_info_repository_mock_data_script(py_i18n_info_repository_mock: Pyi18nInfoInterface):
    _check_script(py_i18n_info_repository_mock)


# def test_py_i18n_info_repository_full_data(py_i18n_info_repository_mock: Pyi18nInfoInterface):
#     repo = Pyi18nInfoRepository(bcp47_mock)
#     assert repo.languages
#     assert repo.scripts
#     assert repo.regions
#     assert repo.ext_langs
#     assert repo.variants
#     assert repo.grandfathered
#     assert repo.redundant