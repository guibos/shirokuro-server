from datetime import datetime

import pytest
from pydantic_core import Url

from internationalization.repositories.bcp47.bcp47_interface import BCP47Interface
from internationalization.repositories.bcp47.exceptions.script_subtag_not_found_error import ScriptSubtagNotFoundError
from internationalization.repositories.py_i18n_info.py_i18n_info_interface import Pyi18nInfoInterface
from internationalization.repositories.py_i18n_info.py_i18n_info_repository import Pyi18nInfoRepository
from internationalization.repositories.py_i18n_info.schemas.py_i18n_info_subtags import Pyi18nInfoSubtags


@pytest.fixture(scope="session")
def py_i18n_info_repository_mock(bcp47_mock: BCP47Interface) -> Pyi18nInfoInterface:
    return Pyi18nInfoRepository(bcp47_mock)


def test_py_i18n_info_repository_search_case_sensitive(py_i18n_info_repository_mock: Pyi18nInfoInterface):
    with pytest.raises(ScriptSubtagNotFoundError):
        py_i18n_info_repository_mock.get_script_by_subtag('latn', case_sensitive=True)

    latin = py_i18n_info_repository_mock.get_script_by_subtag('Latn', case_sensitive=True)
    assert latin.subtag == 'Latn'


def test_py_i18n_info_repository_search_case_insensitive(py_i18n_info_repository_mock: Pyi18nInfoInterface):
    latin = py_i18n_info_repository_mock.get_script_by_subtag('latn', case_sensitive=False)
    assert latin.subtag == 'Latn'

    latin = py_i18n_info_repository_mock.get_script_by_subtag('Latn', case_sensitive=False)
    assert latin.subtag == 'Latn'


def test_py_i18n_info_repository_latin_script(py_i18n_info_repository_mock: Pyi18nInfoInterface):
    latin = py_i18n_info_repository_mock.get_script_by_subtag('Latn')

    english = py_i18n_info_repository_mock.get_language_by_subtag('en')
    united_kingdom = py_i18n_info_repository_mock.get_region_by_subtag('GB')
    subtag_english_uk = Pyi18nInfoSubtags(language=english, region=united_kingdom)
    subtag_english = Pyi18nInfoSubtags(language=english, )

    assert latin.id is None
    assert latin.source_data == Url('http://www.wikidata.org/entity/Q8229')
    assert len(latin.i18n_info) == 2
    assert latin.i18n_info[subtag_english_uk].name == 'Latin script'
    assert latin.i18n_info[subtag_english_uk].description
    assert latin.i18n_info[subtag_english].name == 'Latin script'
    assert latin.i18n_info[subtag_english].description
    assert latin.description == ['Latin']
    assert latin.added == datetime(2005, 10, 16, 0, 0)
    assert latin.updated_at
    assert latin.subtag == 'Latn'
    assert latin.comments is None


def test_py_i18n_info_repository_with_comments(py_i18n_info_repository_mock: Pyi18nInfoInterface):
    inherits_scripts = py_i18n_info_repository_mock.get_script_by_subtag('Zinh')
    assert inherits_scripts.comments
