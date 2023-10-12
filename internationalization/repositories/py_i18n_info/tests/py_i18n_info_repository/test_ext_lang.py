from datetime import datetime

import pytest
from pydantic_core import Url

from internationalization.repositories.py_i18n_info.exceptions.py_i18n_info_ext_lang_subtag_not_found_error import \
    Pyi18nInfoExtLangSubtagNotFoundError
from internationalization.repositories.py_i18n_info.py_i18n_info_interface import Pyi18nInfoInterface
from internationalization.repositories.py_i18n_info.schemas.py_i18n_info_ext_lang import Pyi18nInfoExtLang, \
    Pyi18nInfoExtLangPreferredValue, Pyi18nInfoExtLangPrefix
from internationalization.repositories.py_i18n_info.schemas.py_i18n_info_subtags import Pyi18nInfoSubtags


def test_py_i18n_info_repository_ext_lang_list(py_i18n_info_repository_mock: Pyi18nInfoInterface):
    assert py_i18n_info_repository_mock.ext_langs

    for ext_lang in py_i18n_info_repository_mock.ext_langs:
        assert type(ext_lang) == Pyi18nInfoExtLang


def test_py_i18n_info_repository_ext_lang_get_by_tag_insensitive(py_i18n_info_repository_mock: Pyi18nInfoInterface):
    assert py_i18n_info_repository_mock.get_ext_lang_by_subtag('en')
    assert py_i18n_info_repository_mock.get_ext_lang_by_subtag('EN')


def test_py_i18n_info_repository_ext_lang_get_by_tag_not_found(py_i18n_info_repository_mock: Pyi18nInfoInterface):
    with pytest.raises(Pyi18nInfoExtLangSubtagNotFoundError):
        py_i18n_info_repository_mock.get_ext_lang_by_subtag('ERROR')


def test_py_i18n_info_repository_ext_lang_id(py_i18n_info_repository_mock: Pyi18nInfoInterface):
    for ext_lang in py_i18n_info_repository_mock.ext_langs:
        assert ext_lang.id is None


def test_py_i18n_info_repository_ext_lang_description(py_i18n_info_repository_mock: Pyi18nInfoInterface):
    english = py_i18n_info_repository_mock.get_ext_lang_by_subtag('en')
    f1 = py_i18n_info_repository_mock.get_ext_lang_by_subtag('f1')

    assert english.description == ['Ext lang 1']
    assert f1.description == ['Ext lang 2', '2']


def test_py_i18n_info_repository_ext_lang_deprecated(py_i18n_info_repository_mock: Pyi18nInfoInterface):
    english = py_i18n_info_repository_mock.get_ext_lang_by_subtag('en')
    f1 = py_i18n_info_repository_mock.get_ext_lang_by_subtag('f1')

    assert english.deprecated is None
    assert f1.deprecated == datetime(2010, 7, 29, 0, 0)


def test_py_i18n_info_repository_ext_lang_updated_at(py_i18n_info_repository_mock: Pyi18nInfoInterface):
    english = py_i18n_info_repository_mock.get_ext_lang_by_subtag('en')
    assert english.updated_at == datetime(2023, 8, 2, 0, 0)


def test_py_i18n_info_repository_ext_lang_subtag(py_i18n_info_repository_mock: Pyi18nInfoInterface):
    english = py_i18n_info_repository_mock.get_ext_lang_by_subtag('en')
    assert english.subtag == 'en'


def test_py_i18n_info_repository_ext_lang_preferred_value(py_i18n_info_repository_mock: Pyi18nInfoInterface):
    lang_en = py_i18n_info_repository_mock.get_language_by_subtag('en')
    english = py_i18n_info_repository_mock.get_ext_lang_by_subtag('en')

    assert english.preferred_value == Pyi18nInfoExtLangPreferredValue(language=lang_en)


def test_py_i18n_info_repository_ext_lang_prefix(py_i18n_info_repository_mock: Pyi18nInfoInterface):
    lang_fake = py_i18n_info_repository_mock.get_language_by_subtag('f1')
    language_austro_asiatic = py_i18n_info_repository_mock.get_language_by_subtag('aav')
    english = py_i18n_info_repository_mock.get_ext_lang_by_subtag('en')
    f1 = py_i18n_info_repository_mock.get_ext_lang_by_subtag('f1')

    assert english.prefix == []
    assert f1.prefix == [Pyi18nInfoExtLangPrefix(language=lang_fake), Pyi18nInfoExtLangPrefix(language=language_austro_asiatic)]


def test_py_i18n_info_repository_ext_lang_macro_language(py_i18n_info_repository_mock: Pyi18nInfoInterface):
    language_austro_asiatic = py_i18n_info_repository_mock.get_language_by_subtag('aav')
    english = py_i18n_info_repository_mock.get_ext_lang_by_subtag('en')
    f1 = py_i18n_info_repository_mock.get_ext_lang_by_subtag('f1')

    assert english.macro_language is None
    assert f1.macro_language == language_austro_asiatic


def test_py_i18n_info_repository_ext_lang_source_data(py_i18n_info_repository_mock: Pyi18nInfoInterface):
    english = py_i18n_info_repository_mock.get_ext_lang_by_subtag('en')
    f1 = py_i18n_info_repository_mock.get_ext_lang_by_subtag('f1')

    assert english.source_data == Url('http://www.wikidata.org/entity/Q1860')
    assert f1.source_data is None
    # Note: I not possible to provide any case for source_data is None, there are too many restriction.


def test_py_i18n_info_repository_ext_lang_i18n(py_i18n_info_repository_mock: Pyi18nInfoInterface):
    english = py_i18n_info_repository_mock.get_ext_lang_by_subtag('en')
    english_lang = py_i18n_info_repository_mock.get_language_by_subtag('en')
    tag_english = Pyi18nInfoSubtags(language=english_lang, )
    united_kingdom = py_i18n_info_repository_mock.get_region_by_subtag('GB')
    tag_english_uk = Pyi18nInfoSubtags(language=english_lang, region=united_kingdom)

    f1 = py_i18n_info_repository_mock.get_ext_lang_by_subtag('f1')

    assert len(f1.i18n_info) == 0

    assert len(english.i18n_info) == 2
    assert english.i18n_info[tag_english].name == 'English'
    assert english.i18n_info[tag_english].description == 'West Germanic language'
    assert english.i18n_info[tag_english_uk].name == 'English'
    assert english.i18n_info[tag_english_uk].description == 'West Germanic language originating in England'
