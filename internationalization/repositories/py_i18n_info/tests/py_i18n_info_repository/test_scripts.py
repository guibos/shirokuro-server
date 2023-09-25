from datetime import datetime

import pytest
from pydantic_core import Url

from internationalization.repositories.bcp47.exceptions.script_subtag_not_found_error import ScriptSubtagNotFoundError
from internationalization.repositories.py_i18n_info.py_i18n_info_interface import Pyi18nInfoInterface
from internationalization.repositories.py_i18n_info.schemas.py_i18n_info_language import Pyi18nInfoLanguage
from internationalization.repositories.py_i18n_info.schemas.py_i18n_info_subtags import Pyi18nInfoSubtags


def test_py_i18n_info_repository_script_list(py_i18n_info_repository_mock: Pyi18nInfoInterface):
    assert py_i18n_info_repository_mock.scripts

    for script in py_i18n_info_repository_mock.scripts:
        assert type(script) == Pyi18nInfoLanguage


def test_py_i18n_info_repository_script_get_by_subtag_case_insensitive(
        py_i18n_info_repository_mock: Pyi18nInfoInterface):
    latin = py_i18n_info_repository_mock.get_script_by_subtag('latn', case_sensitive=False)
    assert latin.subtag == 'Latn'

    latin = py_i18n_info_repository_mock.get_script_by_subtag('Latn', case_sensitive=False)
    assert latin.subtag == 'Latn'


def test_py_i18n_info_repository_script_get_by_subtag_not_found(py_i18n_info_repository_mock: Pyi18nInfoInterface):
    with pytest.raises(ScriptSubtagNotFoundError):
        py_i18n_info_repository_mock.get_script_by_subtag('Err')


def test_py_i18n_info_repository_script_get_by_subtag_case_sensitive(py_i18n_info_repository_mock: Pyi18nInfoInterface):
    with pytest.raises(ScriptSubtagNotFoundError):
        py_i18n_info_repository_mock.get_script_by_subtag('latn', case_sensitive=True)

    latin = py_i18n_info_repository_mock.get_script_by_subtag('Latn', case_sensitive=True)
    assert latin.subtag == 'Latn'


def test_py_i18n_info_repository_script_id(py_i18n_info_repository_mock: Pyi18nInfoInterface):
    for script in py_i18n_info_repository_mock.scripts:
        assert script.id is None


def test_py_i18n_info_repository_script_source_data(py_i18n_info_repository_mock: Pyi18nInfoInterface):
    latin = py_i18n_info_repository_mock.get_script_by_subtag('Latn')
    fake = py_i18n_info_repository_mock.get_script_by_subtag('Fake')

    assert latin.source_data == Url('http://www.wikidata.org/entity/Q8229')
    assert fake.source_data is None


def test_py_i18n_info_repository_script_i18n_info(py_i18n_info_repository_mock: Pyi18nInfoInterface):
    latin = py_i18n_info_repository_mock.get_script_by_subtag('Latn')
    fake = py_i18n_info_repository_mock.get_script_by_subtag('Fake')

    english = py_i18n_info_repository_mock.get_language_by_subtag('en')
    united_kingdom = py_i18n_info_repository_mock.get_region_by_subtag('GB')
    subtag_english_uk = Pyi18nInfoSubtags(language=english, region=united_kingdom)
    subtag_english = Pyi18nInfoSubtags(language=english, )

    assert len(latin.i18n_info) == 2
    assert fake.i18n_info == {}
    assert latin.i18n_info[subtag_english_uk].name == 'Latin script'
    assert latin.i18n_info[
        subtag_english_uk].description == 'writing system used to write most Western and Central European languages'
    assert latin.i18n_info[subtag_english].name == 'Latin script'
    assert latin.i18n_info[
        subtag_english].description == 'writing system used to write most Western and Central European languages'


def test_py_i18n_info_repository_script_description(py_i18n_info_repository_mock: Pyi18nInfoInterface):
    latin = py_i18n_info_repository_mock.get_script_by_subtag('Latn')
    assert latin.description == ['Latin']

    fake = py_i18n_info_repository_mock.get_script_by_subtag('Fake')
    assert fake.description == ['Fake script', 'Another Fake Script']


def test_py_i18n_info_repository_script_added(py_i18n_info_repository_mock: Pyi18nInfoInterface):
    latin = py_i18n_info_repository_mock.get_script_by_subtag('Latn')
    assert latin.added == datetime(2005, 10, 16, 0, 0)


def test_py_i18n_info_repository_script_updated_at(py_i18n_info_repository_mock: Pyi18nInfoInterface):
    latin = py_i18n_info_repository_mock.get_script_by_subtag('Latn')
    assert latin.updated_at


def test_py_i18n_info_repository_script_subtag(py_i18n_info_repository_mock: Pyi18nInfoInterface):
    latin = py_i18n_info_repository_mock.get_script_by_subtag('Latn')
    assert latin.subtag


def test_py_i18n_info_repository_script_comments(py_i18n_info_repository_mock: Pyi18nInfoInterface):
    latin = py_i18n_info_repository_mock.get_script_by_subtag('Latn')
    assert latin.comments is None

    fake = py_i18n_info_repository_mock.get_script_by_subtag('Fake')
    assert fake.comments == "Fake script to test"
