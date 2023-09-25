import pytest

from internationalization.repositories.py_i18n_info.py_i18n_info_interface import Pyi18nInfoInterface
from internationalization.repositories.py_i18n_info.py_i18n_info_repository import Pyi18nInfoRepository


@pytest.fixture(scope="session")
def py_i18n_info_repository() -> Pyi18nInfoInterface:
    return Pyi18nInfoRepository(
        bcp47_repository
    )  # FIXME: there is a problem with conftest scope. It should be fixed when migrate this code to a new project,
