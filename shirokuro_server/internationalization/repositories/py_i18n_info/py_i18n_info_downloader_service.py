import logging
import os
import urllib.request
from urllib.error import HTTPError

import rdflib
import time
from rdflib.query import ResultRow

from internationalization.repositories.bcp47.bcp47_interface import BCP47Interface
from internationalization.repositories.py_i18n_info._py_i18n_info_base import Pyi18nInfoBase


class Pyi18nInfoDownloaderService(Pyi18nInfoBase):
    _WIKIDATA_ENDPOINT = 'https://www.wikidata.org/wiki/Special:EntityData/{id}.ttl?flavor=simple'
    _SPARQL_QUERY_BCP47_LANGUAGE = "internationalization/repositories/py_i18n_info/queries/"\
                                   "get_languages_resources_urls.rq"
    _SPARQL_QUERY_BCP47_SCRIPT = "internationalization/repositories/py_i18n_info/queries/get_scripts_resources_urls.rq"
    _SPARQL_QUERY_BCP47_REGION = "internationalization/repositories/py_i18n_info/queries/get_regions_resources_urls.rq"
    _SPARQL_QUERY_BCP47_VARIANT = "internationalization/repositories/py_i18n_info/queries/get_variants_resources_urls.rq"

    TEST_MODE_ITERATIONS = 2

    def __init__(self, bcp47_repository: BCP47Interface):
        self._logger = logging.getLogger()
        self._logger.setLevel("INFO")
        self._bcp47_repository = bcp47_repository

    def download(self, *, replace_semantic_data: bool, test_mode: bool = False):
        g = rdflib.Graph()
        for query, data_dir, last_subtag in [
            [self._get_region_query(), self._SEMANTIC_REGION_DATA_DIR, False],
            [self._get_script_query(), self._SEMANTIC_SCRIPT_DATA_DIR, False],
            [self._get_language_query(), self._SEMANTIC_LANGUAGE_DATA_DIR, False],
            [self._get_variant_query(), self._SEMANTIC_VARIANT_DATA_DIR, True]
        ]:
            sparql_result = g.query(query)

            i = 0

            for result_row in sparql_result:
                self._download_result_result_row(result_row, data_dir, replace_semantic_data, last_subtag)

                i += 1
                if test_mode and self.TEST_MODE_ITERATIONS <= i:
                    break

    def _get_region_query(self):
        with open(self._SPARQL_QUERY_BCP47_REGION, 'r') as f:
            return f.read()

    def _get_script_query(self):
        with open(self._SPARQL_QUERY_BCP47_SCRIPT, 'r') as f:
            return f.read()

    def _get_language_query(self):
        with open(self._SPARQL_QUERY_BCP47_LANGUAGE, 'r') as f:
            return f.read()

    def _get_variant_query(self):
        with open(self._SPARQL_QUERY_BCP47_VARIANT, 'r') as f:
            query = f.read()
        filters = (f"contains(?bcp47, '{variant.subtag}')" for variant in self._bcp47_repository.variants)
        full_filter = ' || '.join(filters)
        return query % full_filter

    def _download_result_result_row(self, result_row: ResultRow, data_dir: str, replace_semantic_data: bool,
                                    last_subtag: bool):
        if last_subtag:
            tag = result_row[1].split('-')[-1]
        else:
            tag = result_row[1]

        path = os.path.join(data_dir, self._SEMANTIC_PREFIX_FILE + tag) + self._SEMANTIC_EXTENSION_FILE
        if os.path.isfile(path) and not replace_semantic_data:
            return
        url = self._WIKIDATA_ENDPOINT.format(id=result_row.item.rsplit('/', 1)[-1])
        self._logger.info('Downloading: "%s".', url)
        print('Downloading: "%s".', url)
        try:
            urllib.request.urlretrieve(url, path)
        except HTTPError as e:
            sleep_time = int(e.headers.get('retry-after'))
            print('Retry policy: awaiting %s seconds.', sleep_time, url)
            self._logger.warning('Retry policy: awaiting %s seconds.', sleep_time, url)
            time.sleep(sleep_time)
            urllib.request.urlretrieve(url, path)
