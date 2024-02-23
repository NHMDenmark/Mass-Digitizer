# -*- coding: utf-8 -*-
"""
  Created on 2022-06-21
  @author: Jan K. Legind, NHMD
  Copyright 2022 Natural History Museum of Denmark (NHMD)
  Licensed under the Apache License, Version 2.0 (the "License");
  you may not use this file except in compliance with the License.
  You may obtain a copy of the License at
  http://www.apache.org/licenses/LICENSE-2.0
  Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for the specific language governing permissions and limitations under the License.

  PURPOSE: Transform table with specify imports into a spreadsheet with drop-downs for each name row.
"""
import xlsxwriter
import pandas as pd
import sqlite3
import sys
import string

con = sqlite3.connect(r'C:\DaSSCo\db.sqlite3') #Please set the connection to the operational database (SQLite assumed).
# Will like be this type of path: C:\Users\Swedish_license_plate\OneDrive - University of Copenhagen\Documents\DaSSCo\db.sqlite3
# storagetxt = ''
workbook = xlsxwriter.Workbook("authorDropdown02.xlsx") # Output Excel sheet and set name
worksheet = workbook.add_worksheet() # Global worksheet used throughout


def createDF_fromSQL(con, sql):
    '''
    You must have a table that is the product of a join between say Specify Botany export, and the Digi app taxon table.
    The resulting table should have columns [genus, species, storage, binomial, and author]. This process is explained in
    https://github.com/NHMDenmark/Mass-Digitizer/issues/460#issuecomment-1935723916
    orderColumn: Check for the exact name - could be shelf or box
    storageName: Can be 'box', 'shelf', 'vial' and a few more. For C-Danish herbarium it is 'Box'.
    :return: A dataframe based on the SQL query
    '''
    # global storagetxt
    # storagetxt = storageName
    df = pd.read_sql_query(sql, con)  # Notice the ordering - it can be by storage if necessary
    return df

# Replace commas in author names to prevent unwanted excel behavior (newlines)
def commaReplace(element, replacement='٬'):
    lcomp = [w.replace(',', replacement) for w in element]
    joined = ''.join(lcomp)
    return joined

def authorsToDropDowns(worksheet, author_List, columnPosition):
    #columnTitles must be a list of three
    #columnPosition should be G or later in the alphabet to make space for the new taxonomic group.
    def assignDropdowns(columnPosition, authors):
        counter = 1
        for j in authors:
            j = list(set(j))
            counter += 1 #Counter used to set the row number
            cellValue = f"{columnPosition}{counter}"
            worksheet.data_validation(cellValue, {"validate": "list", "source": j})

    assignDropdowns(columnPosition, author_List)

# Create the data frames needed for the spreadsheet dropdown process
speciesSQL = f'SELECT taxonid, box, name, authors FROM species_authors ORDER BY box;' # Notice table species-author
speciesDf = createDF_fromSQL(con, speciesSQL) # Make sure to order by the column that fits the workflow the best. I assume it is storage name (for Vascular plants= 'Box')
print('-------------------')
print(speciesDf.head(10).to_string())
#
## SPECIES Data Frame SECTION
# Below a new column is added containing the author names grouped by binomial name.
def processSpeciesDf(speciesDf):
    # This function takes a data frame and does operations on it
    # Returns: Processed data frame
    speciesDf['authors'] = speciesDf['authors'].apply(commaReplace)
    speciesDf['authorlist'] = speciesDf.groupby(['box','name'])['authors'].transform(lambda x: [list(x) for v in x])

    def changeDelimiter(item, delimiter=';'):
        return item[0].split(delimiter)

    speciesDf['authorlist'] = speciesDf['authorlist'].apply(changeDelimiter)
    return speciesDf

# Create species lists for populating the worksheet SECTION
speciesDf = processSpeciesDf(speciesDf)

speciesTaxonidList = speciesDf['taxonid'].to_list()
speciesBoxList = speciesDf['box'].to_list()
speciesBoxList = [f'Box {x}' for x in speciesBoxList]
speciesNameList = speciesDf['name'].to_list()

speciesAuthorList = speciesDf['authorlist'].to_list()
authorsToDropDowns(worksheet, speciesAuthorList, 'C') # The species author drop-down is placed in column C
# END species lists section /

# START GENUS SECTION
def genusDelimiter(item, delimiter=';'):
    return item.split(delimiter)

def uniquify_list(nameList):
    # Removes duplicates from a list
    return list(set(nameList))

genusAuthorSQL = """SELECT taxonid, box, name, authors FROM genus_authors ORDER BY box"""
genusDF = pd.read_sql_query(genusAuthorSQL, con)  # Notice the ordering - it can be by storage if necessary
genusDF['authors'] = genusDF['authors'].apply(commaReplace)
genusDF['authors'] = genusDF['authors'].apply(genusDelimiter)
# genusDF['authorlist'] = genusDF.groupby(['box', 'name'])['authors'].transform(lambda x: [list(x) for v in x])
genusDF['authorlist'] = genusDF['authors'].apply(uniquify_list)

# END genus section /


print('$$$$$$$$$$$$$$$$$$$')
# Begin GENUS list section
# def
print(genusDF['authorlist'].head(3))
genusBoxList = genusDF['box'].to_list()
genusBoxList = [f'Box {x}' for x in genusBoxList]
# sys.exit(0)
genusNameList = genusDF['name'].to_list()
genusAuthor_list = genusDF['authors'].to_list()
genusTaxonid_list = genusDF['taxonid'].to_list()
# END genus list section /

header_format = workbook.add_format(
    {
        "border": 1,
        "bg_color": "#C6E5CE",
        "bold": True,
        "text_wrap": True,
        "valign": "vcenter",
        "indent": 1,
    }
)

genus_header = workbook.add_format(
    {
        "border": 1,
        "bg_color": "#BBE2E4",
        "bold": True,
        "text_wrap": True,
        "valign": "vcenter",
        "indent": 1,
    }
)

# Set up layout of the worksheet.
worksheet.set_column("A:A", 10) #Size of columns
worksheet.set_column("B:B", 25)
worksheet.set_column("C:C", 25)
worksheet.set_column("D:D", 10)
worksheet.set_column("E:E", 25)
worksheet.set_column("F:F", 15)
worksheet.set_column("G:G", 25)
worksheet.set_column("H:H", 25)
worksheet.set_column("J:J", 25)
# Species names section
worksheet.write("A1", "Storage name", header_format)
worksheet.write("B1", "Species name", header_format)
worksheet.write("C1", "Author drop down", header_format)
worksheet.write("D1", "Taxon ID", header_format)
worksheet.write("E1", "Comments", header_format)
worksheet.write_column(1, 0, speciesBoxList)
worksheet.write_column(1, 1, speciesNameList)
worksheet.write_column(1, 3, speciesTaxonidList)
#  End Species names section/
#  Genus names section
genusNameColumn = 'G'
genusAuthorColumn = 'H'
genusBoxColumn = 'F'
genusTaxonIDcolumn = 'I'
worksheet.write("H1", "Author drop down", genus_header)
worksheet.write(f"{genusBoxColumn}1", "Storage name", genus_header)
worksheet.write_column(1, 5, genusBoxList)
worksheet.write(f"{genusNameColumn}1", "Genus", genus_header)
worksheet.write_column(1, 6, genusNameList)
authorsToDropDowns(worksheet, genusAuthor_list, genusAuthorColumn)
worksheet.write(f"{genusTaxonIDcolumn}1", "Taxon ID", genus_header)
worksheet.write_column(1, 8, genusTaxonid_list)
worksheet.write("J1", "Comments", genus_header)

#  End Genus names section/

# TEST PART !!!!!!!!!!
import random
def lengthDataframe(a_dataframe):
    # Returns the number of rows in DF as int.
    # Shall pick several random names from the SQLite DB taxonname table and test if the authors attached to that name are present in the speciesDataframe.
    lenDF = len(a_dataframe.index)
    return lenDF


def run_testSuite(my_dataFrame, number_of_runs, rankid):
    # my_dataFrame is either speciesDf or genusDF
    dfLength = lengthDataframe(my_dataFrame)
    for j in range(number_of_runs):
        randomIndex = random.randint(1, dfLength)
        randRow = my_dataFrame.iloc[[randomIndex]] # The random row to be tested on

        taxonName_for_test = list(randRow['name'])
        tst_name = f"'{taxonName_for_test[0]}'"
        pandasAuthors = list(randRow['authorlist'])[0]

        sql_for_test = f'SELECT author, t.name FROM taxonname t WHERE t.rankid = {rankid} AND t.name = {tst_name} AND length(author) > 0;'
        # Based on the random name the SQL query should yield author and name
        dfFromSQL = pd.read_sql_query(sql_for_test, con)
        print("---------------------")
        test_name = dfFromSQL['name'].to_list()[0]
        test_authors = dfFromSQL['author'].to_list()[0]
        test_authors = commaReplace(test_authors)
        print(test_name) # V
        print(test_authors) # V
        sp_name = my_dataFrame[my_dataFrame['name'] == test_name]
        sp_authors = sp_name['authorlist']
        spAuthorList = sp_authors.to_list()[0]
        # test_authors = 'oiuy345' # If you want to force a failed test!

        if test_authors in spAuthorList:
            print("TEST passed successfully")
        else:
            import ctypes
            print(f"{test_authors} not in {spAuthorList}")
            ctypes.windll.user32.MessageBoxW(None, u"Error! Author NOT found--", u"Error", 0)
            sys.exit(1)
run_testSuite(speciesDf, 10, 220) # rankid is either 180 (genus) or 220 (species)
run_testSuite(genusDF, 10, 180) # Testing genusDF
# If test suite is successful then Excel sheet is created.
workbook.close()


