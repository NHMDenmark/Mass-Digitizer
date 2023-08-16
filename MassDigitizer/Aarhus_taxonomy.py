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
import data_access

db = data_access.DataAccess()
cur = db.getDbCursor()

aaDF = pd.read_excel('Aarhus.xls', index_col=None, na_filter=False) #Original NHMA Entomologi taxonomy



specimen = {'taxonid': 0, 'superfamily':'', 'family':'', 'genus': '', 'species': '', 'author':''}

superFamily = ''
family = ''
genus = ''
species = ''
author = ''
finalList = []

##Make this conditional somehow so that the Aarhus.xls is not read and processed every time.

###

def parseAarhus(spreadsheet):
    # Turn the Aarhus NHMA Entomology taxonomy Excel sheet into atomic records
    arhusTax = pd.read_excel(spreadsheet, index_col=None, na_filter=False)
    sortnr = list(arhusTax['Sortnr'])  # Sortnr is the same as taxonomic ID in NHMA parlance.
    sortNr = [j // 10 for j in sortnr]  # The ID was submitted with a zero tagged on to the genuine ID

    AaRanks = list(arhusTax['TYPE'])
    AaNames = list(arhusTax['NAME'])
    AaAuthors = list(arhusTax['AUTOR'])
    zipAa = list(zip(sortNr, AaRanks, AaNames,
                     AaAuthors))
    # Creates a list of tuples that will populate the taxonomic records (specimen)

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

    refinedDF = pd.DataFrame(finalList)
    return refinedDF
# AaDF = pd.DataFrame(finalList)
arhusdf = parseAarhus('Aarhus.xls')
print(arhusdf.head(60).to_string())
def coalesceDF(df):
    # Populates a dataframe with column SPID and fullname

    # Add empty binomial column to df
    df.insert(6, 'binomial', '')

    # Adds new column 'binomial' with the first name read from right to left.
    df['binomial'] = df[['genus', 'species']].apply(lambda x: ' '.join(x.dropna()), axis=1)
    # Iterate over each row
    for index, rows in df.iterrows():
        # Create list for the current row
        my_list = [rows.superfamily, rows.family, rows.genus]
        my_list = [x for x in my_list if x != ''] #Keep items with content only.

        # Below is codeblock for assigning suprefamily and family to the binomial column.
        myLength = len(my_list)
        if myLength == 1: #Must be superfamily.
            df.at[index,'binomial'] = my_list[0]
            print('len = 1 so binomial::', my_list[0])
        if myLength == 2:#Consequently must be family.
            df.at[index, 'binomial'] = my_list[1]
            print('len = 2 so binomial::', my_list[1])

    return df

res = coalesceDF(arhusdf)
print(res.head(20).to_string())
# res.to_excel("ArhusTaxonomy_w_binomial.xls")
def spidLookup(name):
    #Looks up spid based on name and treedefid = 2 (Aarhus - NHMA)

    sql = f"SELECT spid FROM taxonname t WHERE t.fullname = '{name}' and t.treedefid = 2;"
    # print(sql)
    try:
        res = db.executeSqlStatement(sql)
        print("SPID is", res[0]['spid'])
        spid = res[0]['spid']
    except IndexError:
        # print(f"The name {name} wasn't found in the taxonomy. Returning ''.")
        spid = ''
        pass
    return spid

# Add the lookups

# res.reset_index(drop=True, inplace=True)
nameList = list(res['binomial'])
# # res['spid'] = nameList

def createSpidFile(processedDf, fileName):
    # Doing the actual lookups and writing to output file
    ### Write to file in order to avoid the timeconsuming spidLookup step
    spidList = []
    taxonidList = list(processedDf['taxonid'])
    # print(taxonidList[:11])
    joinDF = pd.DataFrame(columns=['spid', 'name', 'taxonid'])
    with open(fileName, "a") as myfile:

        for name in nameList:
            spid = spidLookup(name)
            aTaxonid = taxonidList.pop(0)
            # print("{spid};{name};{aTaxonid}",f"{spid};{name};{aTaxonid}\n")
            joinDF = joinDF.append({'spid':spid, 'name':name, 'taxonid':aTaxonid}, ignore_index=True)
            myfile.write(f"{spid};{name};{aTaxonid}\n")
            spidList.append(spid)

    return joinDF

nm = createSpidFile(res, "check20230816.txt")
print(nm.head(24).to_string())
# ### see below:
# ###-- If spid txt file has been saved previously we use this as it saves a tremendous amount of time in DB lookup
# # rd = open('NHMA_spid_file.txt', 'r')
# # lines = rd.readlines()
# #
# # res['spid'] = lines
# # res['spid'] = res['spid'].str.rstrip()
# ###-- end block
# res['spid'] = spidList
#
# # Last part here creats the NHMAjoin table that is vital to the NHMA taxonomic id lookup.
# conn = dbaccess.getConnection()
# res.to_sql('NHMAjoin', conn, if_exists='replace', index=False ) # Create the join table for NHMA in DB.
# #REMEMBER TO clean out species names with 'sp.'
# ##check to see if table creation was a success
# ras = pd.read_sql('SELECT * FROM nhmajoin', conn)
# print(ras.head(24))
# ##End check

