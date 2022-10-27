import util
import data_access as db

rows = db.getRows('taxonname', 1000)

def test_shrink_dict():
    rows = db.getRows('taxonname', limit=1000)
    # return rows

    fnameDict = {}
    # Loop populates dict with fullname as keys.
    for j in rows:
        fnameDict[j[3]] = ''

    print(len(fnameDict))
    resShrink = util.shrink_dict(fnameDict, 'Pot')
    assert len(resShrink) == 19

def test_convert_dbrow_list():
    res = util.convert_dbrow_list(rows)
    print(res)
    assert res