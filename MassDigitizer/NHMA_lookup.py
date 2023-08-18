import data_access

db = data_access.DataAccess()
def NHMAlookup(id, table='NHMAjoin'):
    #Look up the taxonomic data and builds a taxonomic row
    #Returns : taxonRow
    taxonRow = {'taxonid': 0, 'rankid': 0, 'family':'', 'genus':'', 'species':'', 'name': '','fullname':'', 'parent':'', 'spid': '' }
    sql = f"SELECT taxonid, superfamily, family, genus, species, coalesce as name, genus || ' ' || species as fullname, spid FROM {table} t WHERE t.taxonid = {id};"
    print('NHMA sql:', sql)
    row = db.executeSqlStatement(sql)
    #Code block below assigns variables based on row position
    taxonId = row[0][0]
    superFamily = row[0][1]
    family = row[0][2]
    genus = row[0][3]
    species = row[0][4]
    name = row[0][5]
    fullName = row[0][6]
    # If rank above Genus then fullName defaults to name
    if fullName is None:
        fullName = name
    parent = ''
    spid = row[0][7]

    #Switch to determine rankId and parentName
    rankId = 0
    if not family and not spid :
        rankId = 130
    elif family and not genus:
        rankId = 140
        #Parent name above Genus is not determined. Would require an extra SQL lookup.
    elif genus and not species:
        rankId = 180
        parent = family
    else:
        rankId = 220
        parent = genus

    taxonRow['taxonid'] = taxonId
    taxonRow['rankid'] = rankId
    taxonRow['family'] = family
    taxonRow['genus'] = genus
    taxonRow['species'] = species
    taxonRow['name'] = name
    taxonRow['fullname'] = fullName
    taxonRow['parent'] = parent
    taxonRow['spid'] = spid

    return taxonRow


# res = NHMAlookup(26)
# #
# print('poiu:', [j for j in res])
# print('SPID:', [res[j] for j in res])