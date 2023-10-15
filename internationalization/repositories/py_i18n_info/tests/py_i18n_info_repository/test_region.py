from datetime import datetime

import pytest
from pydantic_core import Url

from internationalization.repositories.py_i18n_info.exceptions.py_i18n_info_region_subtag_not_found_error import \
    Pyi18nInfoRegionSubtagNotFoundError
from internationalization.repositories.py_i18n_info.py_i18n_info_interface import Pyi18nInfoInterface
from internationalization.repositories.py_i18n_info.schemas.abstract.py_i18n_info_translation import \
    Pyi18nInfoTranslation
from internationalization.repositories.py_i18n_info.schemas.py_i18n_info_region import Pyi18nInfoRegionPreferredValue, \
    Pyi18nInfoRegion
from internationalization.repositories.py_i18n_info.schemas.py_i18n_info_subtags import Pyi18nInfoSubtags


def test_py_i18n_info_repository_region_list(py_i18n_info_repository_mock: Pyi18nInfoInterface):
    assert py_i18n_info_repository_mock.regions

    for regions in py_i18n_info_repository_mock.regions:
        assert isinstance(regions, Pyi18nInfoRegion)


def test_py_i18n_info_repository_region_get_by_tag_insensitive(py_i18n_info_repository_mock: Pyi18nInfoInterface):
    assert py_i18n_info_repository_mock.get_region_by_subtag('GB')
    assert py_i18n_info_repository_mock.get_region_by_subtag('gb')


def test_py_i18n_info_repository_region_get_by_tag_not_found(py_i18n_info_repository_mock: Pyi18nInfoInterface):
    with pytest.raises(Pyi18nInfoRegionSubtagNotFoundError):
        py_i18n_info_repository_mock.get_region_by_subtag('ERROR')


def test_py_i18n_info_repository_region_id(py_i18n_info_repository_mock: Pyi18nInfoInterface):
    for region in py_i18n_info_repository_mock.regions:
        assert region.id is None


def test_py_i18n_info_repository_i18n_info(py_i18n_info_repository_mock: Pyi18nInfoInterface):
    gb = py_i18n_info_repository_mock.get_region_by_subtag('GB')
    fake = py_i18n_info_repository_mock.get_region_by_subtag('GB1')

    en = py_i18n_info_repository_mock.get_language_by_subtag('en')

    assert gb.i18n_info == {
        Pyi18nInfoSubtags(language=en):
        Pyi18nInfoTranslation(name='United Kingdom', description='country in north-west Europe'),
        Pyi18nInfoSubtags(language=en, region=gb):
        Pyi18nInfoTranslation(name='United Kingdom', description='country in Western Europe')
    }
    assert fake.i18n_info == {}


def test_py_i18n_info_repository_region_added(py_i18n_info_repository_mock: Pyi18nInfoInterface):
    gb = py_i18n_info_repository_mock.get_region_by_subtag('GB')

    assert gb.added == datetime(2005, 10, 16, 0, 0)


def test_py_i18n_info_repository_region_comments(py_i18n_info_repository_mock: Pyi18nInfoInterface):
    gb = py_i18n_info_repository_mock.get_region_by_subtag('GB')
    fake = py_i18n_info_repository_mock.get_region_by_subtag('GB1')

    assert gb.comments == 'as of 2006-03-29 GB no longer includes the Channel Islands and Isle of Man; see GG, JE, IM'
    assert fake.comments is None


def test_py_i18n_info_repository_region_deprecated(py_i18n_info_repository_mock: Pyi18nInfoInterface):
    gb = py_i18n_info_repository_mock.get_region_by_subtag('GB')
    fake = py_i18n_info_repository_mock.get_region_by_subtag('GB1')

    assert gb.deprecated is None
    assert fake.deprecated == datetime(2021, 8, 2, 0, 0)


def test_py_i18n_info_repository_region_description(py_i18n_info_repository_mock: Pyi18nInfoInterface):
    gb = py_i18n_info_repository_mock.get_region_by_subtag('GB')
    fake = py_i18n_info_repository_mock.get_region_by_subtag('GB1')

    assert gb.description == ['United Kingdom']
    assert fake.description == ['Fake 1', 'Fake Plus']


def test_py_i18n_info_repository_region_iso_3166_1_alpha2(py_i18n_info_repository_mock: Pyi18nInfoInterface):
    gb = py_i18n_info_repository_mock.get_region_by_subtag('GB')
    fake = py_i18n_info_repository_mock.get_region_by_subtag('GB1')

    assert gb.iso3166_1_alpha2 == 'GB'
    assert fake.iso3166_1_alpha2 is None


def test_py_i18n_info_repository_region_iso_3166_1_alpha3(py_i18n_info_repository_mock: Pyi18nInfoInterface):
    gb = py_i18n_info_repository_mock.get_region_by_subtag('GB')
    fake = py_i18n_info_repository_mock.get_region_by_subtag('GB1')

    assert gb.iso3166_1_alpha3 == 'GBR'
    assert fake.iso3166_1_alpha3 is None


def test_py_i18n_info_repository_region_iso_3166_1_numeric(py_i18n_info_repository_mock: Pyi18nInfoInterface):
    gb = py_i18n_info_repository_mock.get_region_by_subtag('GB')
    fake = py_i18n_info_repository_mock.get_region_by_subtag('GB1')

    assert gb.iso3166_1_numeric == 826
    assert fake.iso3166_1_numeric is None


def test_py_i18n_info_repository_region_official_languages(py_i18n_info_repository_mock: Pyi18nInfoInterface):
    gb = py_i18n_info_repository_mock.get_region_by_subtag('GB')
    fake = py_i18n_info_repository_mock.get_region_by_subtag('GB1')

    en = py_i18n_info_repository_mock.get_language_by_subtag('en')

    assert gb.official_languages == [en]
    assert fake.official_languages == []


def test_py_i18n_info_repository_region_preferred_value(py_i18n_info_repository_mock: Pyi18nInfoInterface):
    gb = py_i18n_info_repository_mock.get_region_by_subtag('GB')
    fake = py_i18n_info_repository_mock.get_region_by_subtag('GB1')

    assert gb.preferred_value is None
    assert fake.preferred_value == Pyi18nInfoRegionPreferredValue(region=gb)


def test_py_i18n_info_repository_region_source_data(py_i18n_info_repository_mock: Pyi18nInfoInterface):
    gb = py_i18n_info_repository_mock.get_region_by_subtag('GB')
    fake = py_i18n_info_repository_mock.get_region_by_subtag('GB1')

    assert gb.source_data == Url('http://www.wikidata.org/entity/Q145')
    assert fake.source_data is None


def test_py_i18n_info_repository_region_subtag(py_i18n_info_repository_mock: Pyi18nInfoInterface):
    gb = py_i18n_info_repository_mock.get_region_by_subtag('GB')

    assert gb.subtag == 'GB'


def test_py_i18n_info_repository_region_updated_at(py_i18n_info_repository_mock: Pyi18nInfoInterface):
    gb = py_i18n_info_repository_mock.get_region_by_subtag('GB')

    assert gb.updated_at == datetime(2023, 8, 2, 0, 0)


def test_py_i18n_info_repository_region_used_languages(py_i18n_info_repository_mock: Pyi18nInfoInterface):
    gb = py_i18n_info_repository_mock.get_region_by_subtag('GB')
    fake = py_i18n_info_repository_mock.get_region_by_subtag('GB1')

    en = py_i18n_info_repository_mock.get_language_by_subtag('en')

    assert gb.used_languages == [en]
    assert fake.used_languages == []
