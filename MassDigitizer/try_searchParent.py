import data_access
import global_settings as gs

db = data_access.DataAccess(gs.databaseName)

# res = db.getRows('collection', limit=20)
#
# for j in res:
#     print([k for k in j])
'''filters (Dictionary) :  A dictionary where the key is the field name and the value is the field filter *including operand*!
                                  The operand should be included with the field and any string values should be enclosed in ""
                                  Example: {'rankid': '=180', 'taxonname': '="Felis"', 'taxonid' : 'IS NOT NULL'}
          limit (Integer) : The maximum number of rows - 0 means all rows'''

def searchParentTaxon(taxonName, rankid, treedefid):
    ''' Will climb the taxonname table to get at the family name which is rankid 140
   taxonName: is the desired name to acquire a family name for.
   rankid: is the target rank , in this case 'family' - id = 140
   returns: target higher rank concept
'''

    while (taxonName != rankid): # The logic for this while() makes no sense but serves its purpose to keep going.
        # taxonRankID = 0
        taxonName = f"= '{taxonName}'"
        treedefid_format = f"= '{treedefid}'"
        spTaxon = db.getRowsOnFilters('taxonname', filters={'fullname': taxonName, 'treedefid': treedefid_format})

        for j in spTaxon:
            print([k for k in j])

        if spTaxon is not None:
            taxonRankId = spTaxon[0][4]
            taxonId = spTaxon[0][0]
            taxonName = spTaxon[0][3]
            parentName = spTaxon[0][6]
            # print(' - retrieved parent taxon %s|%s|%s: "%s" ' %(taxonId,taxonRankId,parentId,taxonName))
            if taxonRankId == rankid:
                return taxonName
            elif taxonRankId < 140:
                return None
            else:
                return (searchParentTaxon(parentName, rankid, treedefid))


rr = searchParentTaxon('Rosa abrica', 140, 13)

print(f"The family name is {rr}")