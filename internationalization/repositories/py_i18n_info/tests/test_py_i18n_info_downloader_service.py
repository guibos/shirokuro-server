import os

import pytest
import rdflib

from internationalization.repositories.py_i18n_info.py_i18n_info_downloader_service import Pyi18nInfoDownloaderService


def _check_data(path):
    files = os.listdir(path)

    assert len(files) == Pyi18nInfoDownloaderService.TEST_MODE_ITERATIONS

    for file in files:
        graph = rdflib.Graph()
        assert graph.parse(os.path.join(path, file))


@pytest.mark.download
def test_py_i18n_info_downloader_service(tmp_path):
    region_tmp_path = tmp_path / "region"
    language_tmp_path = tmp_path / "language"
    script_tmp_path = tmp_path / "script"

    for path in (region_tmp_path, language_tmp_path, script_tmp_path):
        os.mkdir(path)

    class Pyi18nInfoDownloaderServiceMock(Pyi18nInfoDownloaderService):
        _SEMANTIC_REGION_DATA_DIR = region_tmp_path
        _SEMANTIC_LANGUAGE_DATA_DIR = language_tmp_path
        _SEMANTIC_SCRIPT_DATA_DIR = script_tmp_path

    Pyi18nInfoDownloaderServiceMock().download(replace_semantic_data=False, test_mode=True)

    for path in (region_tmp_path, language_tmp_path, script_tmp_path):
        _check_data(path)
