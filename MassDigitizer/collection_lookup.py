# -*- coding: utf-8 -*-

"""
Created
on Thu May 26 17:44:00 2022

@authors: Jan K. Legind, NHMD; Fedor A. Steeman NHMD

Copyright 2022 Natural History Museum of Denmark (NHMD)

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing,
software distributed under the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND,
either express or implied. See the License for the specific language governing permissions and limitations under the License.

"""

import data_access

db = data_access.DataAccess()
def NHMAlookup(id, table='NHMAjoin'):
    '''Look up the taxonomic data and builds a taxonomic row similar
    to what is in sqlite table "taxonname"'''
    #Returns : taxonRow
    taxonRow = {'taxonid': 0, 'rankid': 0, 'family':'', 'genus':'', 'species':'', 'name': '','fullname':'', 'parent':'', 'spid': '' }
    sql = f"SELECT taxonid, superfamily, family, genus, species, coalesce as name, genus || ' ' || species as fullname, spid FROM {table} t WHERE t.taxonid = {id};"
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