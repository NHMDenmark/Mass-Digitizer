import specify_sync
import specify_interface
import global_settings as gs
import pytest

baseUrl = "https://specify-test.science.ku.dk/"

gs.baseURL = baseUrl
csrfToken = specify_interface.getCSRFToken()


def est_syncSpecifyCollections():
    res = specify_sync.syncSpecifyCollections(csrfToken)
    assert res

def est_searchParentTaxon():
    res = specify_sync.searchParentTaxon(1286, 200, csrfToken)
    print('search parent ::', res)

est_searchParentTaxon()