# -*- coding: utf-8 -*-
"""
  Created on 2022-06-21
  @author: Jan K. Legind, Fedor Alexander Steeman, NHMD
  Copyright 2022 Natural History Museum of Denmark (NHMD)
  Licensed under the Apache License, Version 2.0 (the "License");
  you may not use this file except in compliance with the License.
  You may obtain a copy of the License at
  http://www.apache.org/licenses/LICENSE-2.0
  Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for the specific language governing permissions and limitations under the License.

  PURPOSE: Converting a specific taxonomic spreadsheet resource from Aarhus Entomology into a SQLite table for NHMD Digi App use.
"""

import pandas as pd
import dataAccess as db


aaDF = pd.read_excel('Aarhus.xls', index_col=None, na_filter=False)
sortnr = list(aaDF['Sortnr']) # Sortnr is the same as taxonomic ID in NHMA parlance.
sortNr = [j//10 for j in sortnr] #The ID was submitted with a zero tagged on to the genuine ID

AaRanks = list(aaDF['TYPE'])
AaNames = list(aaDF['NAME'])
AaAuthors = list(aaDF['AUTOR'])
zipAa = list(zip(sortNr, AaRanks, AaNames, AaAuthors)) # Creates a list of tuples that will populate the taxonomic records (specimen)


specimen = {'taxonid': 0, 'superfamily':'', 'family':'', 'genus': '', 'species': '', 'author':''}

superFamily = ''
family = ''
genus = ''
species = ''
author = ''
finalList = []

for j in zipAa:
    sortNumber = int(j[0]) # Position 0 is ID, 1 is rank, 2 is name, 3 is author
    if j[1] == 'supfam' :
        superFamily = family = genus = species = '' #Each instance of superfamily will reset the record.
        superFamily = j[2]
    if j[1] == 'famil':
        family = genus = species = '' # As above but further down the hierarchy
        family = j[2]
    if j[1] == 'genus':
        genus = species = ''
        genus = j[2]
    if j[1] == 'species':
        species = j[2]
    author = j[3]

    specimen['taxonid'] = sortNumber
    specimen['superfamily'] = superFamily
    specimen['family'] = family
    specimen['genus'] = genus
    specimen['species'] = species
    if author:
        specimen['author'] = author
    else:
        specimen['author'] = ''

    finalList.append(specimen.copy())

AaDF = pd.DataFrame(finalList)

dbaccess = db.DataAccess()

def coalesceDF(df):
    # Populate dataframe with column SPID and fullname
    df = df.replace('', None)
    # Adds new column with the first name read from right to left.
    df['coalesce'] = df[['species', 'genus', 'family', 'superfamily']].bfill(axis='columns')['species']

    # with pd.ExcelWriter('NHMA_to_excel.xlsx') as writer:
    #     df['coalesce'].to_excel(writer, sheet_name='sheet1')
    return df

def spidLookup(name):
    #Looks up spid based on name and treedefid = 2 (Aarhus - NHMA)

    sql = f"SELECT spid FROM taxonname t WHERE t.name = '{name}' and t.treedefid = 2;"

    try:
        res = dbaccess.executeSqlStatement(sql)
        print("SPID is", res[0]['spid'])
        spid = res[0]['spid']
    except IndexError:
        print(f"The name {name} wasn't found in the taxonomy. Returning ''.")
        spid = ''
        pass
    return spid

# Add the lookups
res = coalesceDF(AaDF)
res.reset_index(drop=True, inplace=True)
nameList = list(res['coalesce'])
# res['spid'] = nameList
spidList = []

### Write to file in order to avoid the timeconsuming spidLookup step
with open("test.txt", "a") as myfile:

    for name in nameList:
        spid = spidLookup(name)
        myfile.write(f"{spid}\n")
        spidList.append(spid)
### see below:
###-- If spid txt file has been saved previously we use this as it saves a tremendous amount of time in DB lookup
# rd = open('NHMA_spid_file.txt', 'r')
# lines = rd.readlines()
#
# res['spid'] = lines
# res['spid'] = res['spid'].str.rstrip()
###-- end block
res['spid'] = spidList

conn = dbaccess.getConnection()
res.to_sql('NHMAjoin', conn, if_exists='replace', index=False ) # Create the join table for NHMA in DB.
#REMEMBER TO clean out species names with 'sp.'
##check to see if table creation was a success
ras = pd.read_sql('SELECT * FROM nhmajoin', conn)
print(ras)
##End check

