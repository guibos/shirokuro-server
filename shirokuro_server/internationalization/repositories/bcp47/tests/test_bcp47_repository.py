from internationalization.repositories.bcp47.bcp47_repository import BCP47Repository


def test_bcp_parse():
    bcp47_repository = BCP47Repository()
    assert bcp47_repository.languages
    assert bcp47_repository.scripts
    assert bcp47_repository.regions
    assert bcp47_repository.variants
    assert bcp47_repository.grandfathered
    assert bcp47_repository.redundant
    assert bcp47_repository.ext_langs
