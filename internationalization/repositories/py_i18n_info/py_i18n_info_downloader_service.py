import os
import urllib.request
from urllib.error import HTTPError

import rdflib
import time
from rdflib.query import ResultRow

from internationalization.repositories.py_i18n_info._py_i18n_info_base import Pyi18nInfoBase


class Pyi18nInfoDownloaderService(Pyi18nInfoBase):
    _WIKIDATA_ENDPOINT = 'https://www.wikidata.org/wiki/Special:EntityData/{id}.ttl?flavor=simple'
    _SPARQL_QUERY_BCP47_LANGUAGE = "internationalization/repositories/py_i18n_info/queries/"\
                                   "get_languages_resources_urls.rq"
    _SPARQL_QUERY_BCP47_SCRIPT = "internationalization/repositories/py_i18n_info/queries/get_scripts_resources_urls.rq"
    _SPARQL_QUERY_BCP47_REGION = "internationalization/repositories/py_i18n_info/queries/get_regions_resources_urls.rq"
    _SPARQL_QUERY_BCP47_VARIANT = "internationalization/repositories/py_i18n_info/queries/get_variant_resources_urls.rq"

    TEST_MODE_ITERATIONS = 2

    def download(self, *, replace_semantic_data: bool, test_mode: bool = False):
        g = rdflib.Graph()
        for query_file, data_dir in [
            [self._SPARQL_QUERY_BCP47_REGION, self._SEMANTIC_REGION_DATA_DIR],
            [self._SPARQL_QUERY_BCP47_SCRIPT, self._SEMANTIC_SCRIPT_DATA_DIR],
            [self._SPARQL_QUERY_BCP47_LANGUAGE, self._SEMANTIC_LANGUAGE_DATA_DIR],
                # [self._SPARQL_QUERY_BCP47_VARIANT, self._SEMANTIC_VARIANT_DATA_DIR]
        ]:
            # TODO: It is required to download variants subtags. Problems:
            #   - ISO 639-6 not match with bcp47 subtag
            #   - ISO 639-6 is withdraw
            #   - Wikidata BCP47 field could (or not) include language subtag.
            with open(query_file, 'r') as f:
                query = f.read()
            sparql_result = g.query(query)

            i = 0

            for result_row in sparql_result:
                self._download_result_result_row(result_row, data_dir, replace_semantic_data)

                i += 1
                if test_mode and self.TEST_MODE_ITERATIONS <= i:
                    break

    def _download_result_result_row(self, result_row: ResultRow, data_dir: str, replace_semantic_data: bool):
        path = os.path.join(data_dir, self._SEMANTIC_PREFIX_FILE + result_row[1]) + self._SEMANTIC_EXTENSION_FILE
        if os.path.isfile(path) and not replace_semantic_data:
            return
        url = self._WIKIDATA_ENDPOINT.format(id=result_row.item.rsplit('/', 1)[-1])
        try:
            urllib.request.urlretrieve(url, path)
        except HTTPError as e:
            time.sleep(int(e.headers.get('retry-after')))
            urllib.request.urlretrieve(url, path)
