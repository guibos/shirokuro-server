from datetime import datetime

import pytest
from pydantic_core import Url

from internationalization.repositories.py_i18n_info.exceptions.py_i18n_info_language_subtag_not_found_error import \
    Pyi18nInfoLanguageSubtagNotFoundError
from internationalization.repositories.py_i18n_info.py_i18n_info_interface import Pyi18nInfoInterface
from internationalization.repositories.py_i18n_info.schemas.py_i18n_info_language import Pyi18nInfoLanguage, \
    Pyi18nInfoLanguagePreferredValue
from internationalization.repositories.py_i18n_info.schemas.py_i18n_info_subtags import Pyi18nInfoSubtags


def test_py_i18n_info_repository_language_list(py_i18n_info_repository_mock: Pyi18nInfoInterface):
    assert py_i18n_info_repository_mock.languages

    for language_scope in py_i18n_info_repository_mock.languages:
        assert isinstance(language_scope, Pyi18nInfoLanguage)


def test_py_i18n_info_repository_language_get_by_tag_insensitive(py_i18n_info_repository_mock: Pyi18nInfoInterface):
    assert py_i18n_info_repository_mock.get_language_by_subtag('en')
    assert py_i18n_info_repository_mock.get_language_by_subtag('EN')


def test_py_i18n_info_repository_language_get_by_tag_not_found(py_i18n_info_repository_mock: Pyi18nInfoInterface):
    with pytest.raises(Pyi18nInfoLanguageSubtagNotFoundError):
        py_i18n_info_repository_mock.get_language_by_subtag('ERROR')


def test_py_i18n_info_repository_language_id(py_i18n_info_repository_mock: Pyi18nInfoInterface):
    for language in py_i18n_info_repository_mock.languages:
        assert language.id is None


def test_py_i18n_info_repository_language_added(py_i18n_info_repository_mock: Pyi18nInfoInterface):
    english = py_i18n_info_repository_mock.get_language_by_subtag('en')
    assert english.added == datetime(2005, 10, 16, 0, 0)


def test_py_i18n_info_repository_language_comments(py_i18n_info_repository_mock: Pyi18nInfoInterface):
    english = py_i18n_info_repository_mock.get_language_by_subtag('en')
    assert english.comments is None

    fake = py_i18n_info_repository_mock.get_language_by_subtag('f1')
    assert fake.comments == "Fake language to test"


def test_py_i18n_info_repository_language_deprecated(py_i18n_info_repository_mock: Pyi18nInfoInterface):
    english = py_i18n_info_repository_mock.get_language_by_subtag('en')
    assert english.deprecated is None

    fake = py_i18n_info_repository_mock.get_language_by_subtag('f1')
    assert fake.deprecated == datetime(2023, 8, 2, 0, 0)


def test_py_i18n_info_repository_language_description(py_i18n_info_repository_mock: Pyi18nInfoInterface):
    english = py_i18n_info_repository_mock.get_language_by_subtag('en')
    assert english.description == ['English']

    fake = py_i18n_info_repository_mock.get_language_by_subtag('f1')
    assert fake.description == ['Fake Language', 'Fake Language D']


def test_py_i18n_info_repository_language_i18n_info(py_i18n_info_repository_mock: Pyi18nInfoInterface):
    fake = py_i18n_info_repository_mock.get_language_by_subtag('f1')
    english = py_i18n_info_repository_mock.get_language_by_subtag('en')
    united_kingdom = py_i18n_info_repository_mock.get_region_by_subtag('GB')
    subtag_english_uk = Pyi18nInfoSubtags(language=english, region=united_kingdom)
    subtag_english = Pyi18nInfoSubtags(language=english, )

    assert fake.i18n_info == {}
    assert len(english.i18n_info) == 2
    assert english.i18n_info[subtag_english].name == 'English'
    assert english.i18n_info[subtag_english].description == 'West Germanic language'
    assert english.i18n_info[subtag_english_uk].name == 'English'
    assert english.i18n_info[subtag_english_uk].description == 'West Germanic language originating in England'


def test_py_i18n_info_repository_language_iso_639_1(py_i18n_info_repository_mock: Pyi18nInfoInterface):
    english = py_i18n_info_repository_mock.get_language_by_subtag('en')
    aav = py_i18n_info_repository_mock.get_language_by_subtag('aav')

    assert english.iso_639_1 == 'en'
    assert aav.iso_639_1 is None


def test_py_i18n_info_repository_language_iso_639_2(py_i18n_info_repository_mock: Pyi18nInfoInterface):
    english = py_i18n_info_repository_mock.get_language_by_subtag('en')
    aav = py_i18n_info_repository_mock.get_language_by_subtag('aav')

    assert english.iso_639_2 == 'eng'
    assert aav.iso_639_2 is None


def test_py_i18n_info_repository_language_iso_639_3(py_i18n_info_repository_mock: Pyi18nInfoInterface):
    english = py_i18n_info_repository_mock.get_language_by_subtag('en')
    aav = py_i18n_info_repository_mock.get_language_by_subtag('aav')

    assert english.iso_639_3 == 'eng'
    assert aav.iso_639_3 is None


def test_py_i18n_info_repository_language_iso_639_5(py_i18n_info_repository_mock: Pyi18nInfoInterface):
    english = py_i18n_info_repository_mock.get_language_by_subtag('en')
    aav = py_i18n_info_repository_mock.get_language_by_subtag('aav')

    assert english.iso_639_5 is None
    assert aav.iso_639_5 == 'aav'


def test_py_i18n_info_repository_language_macro_language(py_i18n_info_repository_mock: Pyi18nInfoInterface):
    english = py_i18n_info_repository_mock.get_language_by_subtag('en')
    aav = py_i18n_info_repository_mock.get_language_by_subtag('aav')
    f1 = py_i18n_info_repository_mock.get_language_by_subtag('f1')

    assert english.macro_language is None
    assert f1.macro_language == aav


def test_py_i18n_info_repository_language_preferred_value(py_i18n_info_repository_mock: Pyi18nInfoInterface):
    english = py_i18n_info_repository_mock.get_language_by_subtag('en')
    f1 = py_i18n_info_repository_mock.get_language_by_subtag('f1')

    assert english.preferred_value is None
    assert f1.preferred_value == Pyi18nInfoLanguagePreferredValue(language=english)


def test_py_i18n_info_repository_language_scope(py_i18n_info_repository_mock: Pyi18nInfoInterface):
    english = py_i18n_info_repository_mock.get_language_by_subtag('en')
    aav = py_i18n_info_repository_mock.get_language_by_subtag('aav')

    assert english.scope is None
    assert aav.scope == py_i18n_info_repository_mock.get_language_scope_by_name('collection')


def test_py_i18n_info_repository_language_source_data(py_i18n_info_repository_mock: Pyi18nInfoInterface):
    english = py_i18n_info_repository_mock.get_language_by_subtag('en')
    f1 = py_i18n_info_repository_mock.get_language_by_subtag('f1')

    assert english.source_data == Url('http://www.wikidata.org/entity/Q1860')
    assert f1.scope is None


def test_py_i18n_info_repository_language_subtag(py_i18n_info_repository_mock: Pyi18nInfoInterface):
    english = py_i18n_info_repository_mock.get_language_by_subtag('en')

    assert english.subtag == 'en'


def test_py_i18n_info_repository_language_suppressed_script(py_i18n_info_repository_mock: Pyi18nInfoInterface):
    english = py_i18n_info_repository_mock.get_language_by_subtag('en')
    f1 = py_i18n_info_repository_mock.get_language_by_subtag('f1')
    latin = py_i18n_info_repository_mock.get_script_by_subtag('latn')

    assert english.suppress_script == latin
    assert f1.suppress_script is None


def test_py_i18n_info_repository_language_updated_date(py_i18n_info_repository_mock: Pyi18nInfoInterface):
    for language in py_i18n_info_repository_mock.languages:
        assert type(language.updated_at) == datetime
