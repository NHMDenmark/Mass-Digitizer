# -*- coding: utf-8 -*-
"""
  Created on Tuesday June 14, 2022
  @author: Fedor Alexander Steeman, NHMD
  Copyright 2022 Natural History Museum of Denmark (NHMD)
  Licensed under the Apache License, Version 2.0 (the "License");
  you may not use this file except in compliance with the License.
  You may obtain a copy of the License at
  http://www.apache.org/licenses/LICENSE-2.0
  Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for the specific language governing permissions and limitations under the License.

  PURPOSE: Synchronizing local database with Specify 
"""
from ast import Is, Not
from getpass import getpass
from queue import Empty
import specify_interface as sp
import data_access as db
import global_settings as gs
import util

def syncSpecifyCollections(csrftoken):
    # Function for synchronizing collections between the Specify7 API and the local database 
    # CONTRACT
    #   csrftoken (String) : The CSRF token required during logging in for the session 
    #   RETURNS (Boolean) : True to indicate the jobs was successfully finished
    
    print('Syncing collections with Specify API at: ' + gs.baseURL)
    # Get collection list from Specify7 API
    specifyCollections = sp.getSpecifyObjects('collection', csrftoken)    
    # Search for each entry in local database  
    for i in range(0, len(specifyCollections)):
        spCollection = specifyCollections[i]
        print(' - checking db for collection {%s,"%s"} ...' %(spCollection['id'], spCollection['collectionname']))
        dbCollection = db.getRowsOnFilters('collection', {'spid': '=%s'%spCollection['id']})
        if len(dbCollection)==0:
            # Collection entry not found! Getting discipline info from Sp7API and inserting missing row...
            print(' - Collection entry not found! Inserting missing row...')
            discipline = sp.directAPIcall(spCollection["discipline"], csrftoken)
            fields = {"spid" : spCollection["id"],"name" : '"%s"' % spCollection["collectionname"],"institutionid" : institution[0],"taxontreedefid" : discipline["taxontreedef"].split(r'/')[4]}
            print(db.insertRow('collection', fields))
    return True

def syncTaxonomy(taxontreedefid, csrftoken):
    # Function for synchronizing collections between the Specify7 API and the local database 
    # CONTRACT
    #   taxontreedefid (Integer) : The primary key of the taxon tree definition for the collection in question 
    #   csrftoken (String) : The CSRF token required during logging in for the session 
    #   limit (Integer) :   The maximum depth of taxon ranks during this sweep; 
    #                       This depth depends on the number of ranks defined for the taxon tree in question 
    #                       Default value: 10 
    #   RETURNS (Boolean) : True to indicate the jobs was successfully finished
    print('Syncing taxonomy with Specify7 API at: ' + gs.baseURL)
    
    # First get available ranks for taxon tree in question from Sp7API 
    taxonranks = sp.getSpecifyObjects('taxontreedefitem', csrftoken, 100, 0,{"treedef":str(taxontreedefid)})

    # 1. Sync local database with Specify taxon names  
    addSpecifyTaxonNamesToLocal(taxonranks, taxontreedefid, csrftoken)    

    # TODO 2. Check for changes in Specify taxa (edited, deleted etc.) 

    # TODO 3. Sync taxonomic hierarchy table  
    
    print('Finished syncing taxonomy with Specify...')
    return True

def addSpecifyTaxonNamesToLocal(taxonranks, taxontreedefid, csrftoken):
    
    #TODO Write function contract

    # Sync local database with Specify taxon names  
    #print('*************************************************************')
    print('Checking local database for Specify taxa with taxontree: %d' % taxontreedefid)
    # Loop through each rank, checking whether local DB has an entry for this taxon 
    for rank in taxonranks:
        rankid = rank['rankid']
        rankname = rank['name']
        if rankid > 200:
            print(' Rank %s:"%s" ' %(rankid, rankname))
            #print(' Getting taxa from Specify7 API at: ' + gs.baseURL)

            # Taxon list is split in pages of 1000 to spare bandwidth and avoid timeouts
            page_number = 340  #  
            page_size = 1000 # 
            end_of_list = False
            taxa_inserted = 0
            while end_of_list == False:
                # Fetch first page of taxa from the Specify7 API 
                print(' - Fetching "%s" with limit %d and offset %d ' %('taxa', page_size, page_number*page_size))
                taxonnames = sp.getSpecifyObjects('taxon', csrftoken, page_size, page_number*page_size, {"definition":str(taxontreedefid), "rankid":str(rankid)})
                
                # Safety hatch (to be removed later)
                #if input('continue?') != 'y':return
                
                # Iterate through taxon names retrieved from Specify7 API to check for entries that aren't already present in local app database 
                print(' - Iterating through  %i taxa found'%len(taxonnames))
                for i in range(0, len(taxonnames)):
                    try:
                        id = taxonnames[i]['id']
                        fullname = taxonnames[i]['fullname']
                        name = taxonnames[i]['name']
                        #gs.db_in_memory = True
                        dbTaxonName = db.getRowsOnFilters('taxonname', {'fullname':'="%s"' % fullname, 'taxonid':'=%s' % id, 'taxontreedefid':'=%s'%taxontreedefid}) 
                        print(' - found %d rows for %s:"%s" ' % (len(dbTaxonName), id, fullname))
                        #print('%i'%len(dbTaxonName), end=' ')
                        if len(dbTaxonName)>1:
                            #print('')
                            print('   > located pre-existing duplicate: %d: %s'%(id,fullname))
                        if len(dbTaxonName)==0: 
                            print('   > Taxon %s:"%s" ("%s") [rank: %s] not in DB ' %(id, fullname, name, str(rankid)))
                            # Check wether taxon name is valid
                            taxon_name_valid = True  
                            invalid_name_strings = {'*', ':', '.', 'Incertae'}
                            for s in invalid_name_strings:
                                if name.rfind(s) != -1:
                                    taxon_name_valid = False
                                    break
                            # If taxon name is valid then add to local app database, else skip
                            if taxon_name_valid:
                                classid = 'NULL' 
                                if rankid >= 60:
                                    classid = searchParentTaxon(id, 60, csrftoken)
                                #print('   > Retrieved classid: %s' % str(classid))
                                
                                # Add missing taxon to local database
                                if True: #input('Insert missing taxon into local DB? (y/n/maybe)') == 'y':
                                    if len(db.getRowsOnFilters('taxonname', {'fullname': '="%s"' % fullname})) == 0:
                                        # TODO explain code 
                                        parentId = int(str(taxonnames[i]['parent']).split('/')[4])
                                        parenttaxon = sp.getSpecifyObject('taxon', parentId, csrftoken)
                                        taxonFields = {'taxonid':'%s'%id, 'name':'"%s"'%name, 'fullname':'"%s"'%fullname,'rankid':'%s'%rankid,'classid':'%s'%classid,'taxontreedefid':'%s'%taxontreedefid, 'parentfullname': '"%s"'%parenttaxon['fullname']}
                                        #print('   > Inserting: %s' %taxonFields)
                                        print('   > Inserting: %s:%s'%(id,fullname)) 
                                        db.insertRow('taxonname',taxonFields)#)
                                        taxa_inserted = taxa_inserted + 1 
                                    else: print('   > skipping duplicate: %s'%fullname)
                            else: print('   > skipping invalid taxon name "%s"'%name)
                    except Exception as e:
                        print(e)
                        input('press a key to continue')   
                print('') 
                #print('.', end=' ')
                
                # Check whether we reached the end, otherwise continue
                if len(taxonnames) < page_size: 
                    print('')
                    print(' - %i taxa < page size %i, therefore end of list; escaping...'%(len(taxonnames), page_size))
                    page_number = 0 
                    end_of_list = True
                    break
                else:        
                    page_number = page_number + 1 # Next page 
            print('')
            print(' - Finished rank %s and inserted %i taxa '%(rankname,taxa_inserted))

    # This line needs a comment, just because 

def check_taxon_duplicates(fullname):

    #TODO Write function contract
    
    duplicates = db.getRowsOnFilters('taxonname', {'fullname': '=%s' % fullname})

    if len(duplicates) > 0: return True
    else: return False

def searchParentTaxon(taxonId, rankid, csrftoken):

    #TODO Write function contract
    
    parentId = 'NULL' 
    taxonRankId = 999
    while(taxonRankId > rankid):
        #print(' - taxonRankId: [%s] > [%s] ' %(str(taxonRankId),str(rankid)))
        spTaxon = sp.getSpecifyObject('taxon',taxonId, csrftoken)
        if spTaxon is not Empty:
            taxonRankId = spTaxon['rankid']
            taxonId = spTaxon['id']
            taxonName = spTaxon['fullname']
            parentId = int(str(spTaxon['parent']).split('/')[4])
            #print(' - retrieved parent taxon %s|%s|%s: "%s" ' %(taxonId,taxonRankId,parentId,taxonName))
            if taxonRankId > rankid: taxonId = parentId
        else: 
            print('   > taxon with id %s could not be retrieved! ' % str(taxonId))
            break

    if taxonRankId != rankid: taxonId = 'NULL'

    #print('   > retrieved parent id: %s ' % str(taxonId))

    return taxonId 

def updateSpecifyTaxonNames(taxonranks, taxontreedefid, csrftoken):
    # TODO Sync local database taxon names with those in Specify 
    # 
    # TODO Doesn't work yet due to API PUT call throwing error 403 (Forbidden)

    for rank in taxonranks:
        rankid = rank['rankid']
        rankname = rank['name']
        if rankid > 220: # Restrict to infraspecific taxa 
            print(' - For rank %s:"%s" ' %(rankid, rankname))
            dbTaxonNames = db.getRowsOnFilters('taxonname', {'rankid': '=%s' % rankid, 'taxontreedefid': '=%s' % taxontreedefid, 'taxonid' : 'IS NOT NULL'})
            print(' - checking Specify7 API for %d rows from local DB for rank %s:"%s" ' % (len(dbTaxonNames), rankid, rankname))
            found = False
            for i in range(0, len(dbTaxonNames)):
                id = dbTaxonNames[i]['taxonid']
                fullname = dbTaxonNames[i]['fullname']
                name = dbTaxonNames[i]['name']
                #print(' - checking Specify API for taxon:%s:"%s" ("%s")' %(id, fullname, name))
                spTaxonName = sp.getSpecifyObject('taxon',id, csrftoken)
                if spTaxonName is not Empty:
                    if spTaxonName['fullname'] != fullname:
                        print('  -> taxon(%s) full name "%s" doesn\'t match "%s"' %(id,spTaxonName['fullname'],fullname))
                        
                        # Update Specify with local DB fullname
                        print('  -> updating Specify  for taxon:%s:"%s"' %(id, fullname))
                        spTaxonName['fullname'] = fullname
                        # TODO API PUT command throws 403 Error ("Forbidden")
                        sp.putSpecifyObject('taxon', id, spTaxonName, csrftoken)
                        #if input('continue?') != 'y': break
                        print('UPDATE taxon SET fullname = "%s" WHERE taxonid = %s; ' %(fullname,id))
                else:
                    print('  -> taxon "%s" not found on primary key: %s!' %(fullname, id))


#def syncLocalTaxonHierarchyWithSpecify
    # TODO Sync taxononomic hierarchy table  

# TEST CODE
util.clear()
print('------- Running specify_sync.py --------')
institutions = db.getRows('institution')
#max_instutionid = 
# for institution in institutions:
#     print(institution)
selected_institutionid = 0 # -1
# while selected_institutionid < 0:
selected_institutionid = input('Please choose institution (0-2):')
institution = db.getRowOnId('institution', selected_institutionid)
print(institution[1], institution[2], institution[3])
gs.baseURL = institution[3]

max_tries = 10
while max_tries > 0:
    token = sp.specifyLogin(input('Enter username: '), getpass('Enter password: '), 688130)
    if token != '': break
    else:
        print('Login failed...')
        if input('Try again? (y/n)') == 'n': break
    max_tries = max_tries - 1
    print('Attempts left: %i' % max_tries)
    
choice = input('Sync what? [1] collections [2] taxonomy ')
#choice = "2"
print('Your choice: "%s"' % choice)
if choice == "1": 
    syncSpecifyCollections(token)
elif choice == "2": 
    syncTaxonomy(13, token)
else: 
    print('You are the weakest link. Goodbye! ')

sp.logout(token)

print('----------- done --------------')