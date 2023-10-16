from urllib.request import urlopen

from internationalization.repositories.bcp47._bcp47_base import BCP47Base


class BCP47DownloaderService(BCP47Base):
    _LANGUAGE_SUBTAG_REGISTRY_URL = 'https://www.iana.org/assignments/language-subtag-registry/language-subtag-registry'

    def download(self):
        with open(self._LANGUAGE_SUBTAG_REGISTRY_FILE_PATH, 'w', encoding='utf-8') as f:
            f.write(self._get_data())

    def _get_data(self) -> str:
        with urlopen(self._LANGUAGE_SUBTAG_REGISTRY_URL) as response:
            data = response.read().decode('utf-8')
            if not data:
                raise RuntimeError("Problems to download BCP47 data.")
        return data
