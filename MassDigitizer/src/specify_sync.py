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
import json
from getpass import getpass
import specify_interface as sp
import data_access as db
import util

def specifyLogin(baseURL, username, passwd):
    # Function for logging in to the Specify7 API and getting the CSRF token necessary for further interactions in the session 
    # CONTRACT
    #   baseURL (String) : the base URL for the institution's Specify7 instance
    #   username (String): Specify account user name  
    #   passwd (String) : Specify account password  
    #   RETURNS (String) : The CSRF token necessary for further interactions in the session 
    print('Connecting to Specify7 API...')
    sp.initInstitution(baseURL)
    csrftoken = sp.getCSRFToken()
    csrftoken = sp.login(username, passwd, csrftoken)
    if sp.verifySession(csrftoken):
        return csrftoken
    else:
        return '' 

def specifyLogout(csrftoken):
    # Function for logging out of the Specify7 API again 
    # CONTRACT
    #   csrftoken (String) : The CSRF token required during logging in for the session 
    print('logging out of Specify...')
    sp.logout(csrftoken)

def syncSpecifyCollections(csrftoken):
    # Function for synchronizing collections between the Specify7 API and the local database 
    # CONTRACT
    #   csrftoken (String) : The CSRF token required during logging in for the session 
    print('Syncing collections with Specify...')
    # Get collection list from Specify7 API
    specifyCollections = sp.fetchSpecifyObjects('collection', csrftoken)    
    # Search for each entry in local database  
    for i in range(0, len(specifyCollections)):
        print(' - checking db for collection {%s,"%s"} ...' %(spCollection['id'], spCollection['collectionname']))
        spCollection = specifyCollections[i]
        dbCollection = db.getRowsOnFilters('collection', {'spid': '=%s'%spCollection['id']})
        if len(dbCollection)==0:
            # Collection entry not found! Getting discipline info from Sp7API and inserting missing row...
            discipline = sp.directAPIcall(spCollection["discipline"], csrftoken)
            fields = {"spid" : spCollection["id"],"name" : '"%s"' % spCollection["collectionname"],"institutionid" : institution[0],"taxontreedefid" : discipline["taxontreedef"].split(r'/')[4]}
            print(db.insertRow('collection', fields))

def syncTaxonomy(taxontreedefid, csrftoken, limit=10):
    # Function for synchronizing collections between the Specify7 API and the local database 
    # CONTRACT
    #   taxontreedefid (Integer) : The primary key of the taxon tree definition for the collection in question 
    #   csrftoken (String) : The CSRF token required during logging in for the session 
    #   limit (Integer) :   The maximum depth of taxon ranks during this sweep; 
    #                       This depth depends on the number of ranks defined for the taxon tree in question 
    #                       Default value: 10 
    # TODO Split this function's stages up into separate functions  
    print('Syncing taxonomy with Specify...')
    
    # First get available ranks for taxon tree in question from Sp7API 
    taxonranks = sp.fetchSpecifyObjects('taxontreedefitem', csrftoken, limit, 0,{"treedef":str(taxontreedefid)})

    # 1. Sync local database with Specify taxon names  
    addSpecifyTaxonNamesToLocal(taxonranks, taxontreedefid, csrftoken)    
    # 2. Sync Specify with local DB taxon names  
    addLocalTaxonNamesToSpecify(taxonranks, taxontreedefid, csrftoken)

    # TODO 3. Sync local database taxon names with those in Specify 
    #updateSpecifyTaxonNames(taxonranks, taxontreedefid, csrftoken)

    # TODO 4. Sync taxononomic hierarchy table  
    
    print('Finished syncing taxonomy with Specify...')

def addSpecifyTaxonNamesToLocal(taxonranks, taxontreedefid, csrftoken):
    # Sync local database with Specify taxon names  
    print('*************************************************************')
    print('Checking local database for Specify taxa with taxontree: %d' % taxontreedefid)
    # Loop through each rank, checking whether local DB has an entry for this taxon 
    for rank in taxonranks:
        rankid = rank['rankid']
        rankname = rank['name']
        if rankid > 10:
            print(' Rank %s:"%s" ' %(rankid, rankname))
            taxonnames = sp.fetchSpecifyObjects('taxon', csrftoken, 100,0,{"definition":str(taxontreedefid), "rankid":str(rankid)})
            for i in range(0, len(taxonnames)):
                id = taxonnames[i]['id']
                fullname = taxonnames[i]['fullname']
                name = taxonnames[i]['name']
                dbTaxonName = db.getRowsOnFilters('taxonname', {'fullname':'="%s"' % fullname, 'taxonid':'=%s' % id}) # TODO filter on taxontreedefid !!! 
                #print(' - found %d rows for %s:"%s" ' % (len(dbTaxonNames), id, fullname))
                #print(dbTaxonNames)
                if len(dbTaxonName)==0: 
                    print(' - %s:"%s" ("%s") not in DB ' %(id, fullname, name))
                    # TODO add missing taxon to local database  
    
def addLocalTaxonNamesToSpecify(taxonranks, taxontreedefid, csrftoken):
    # Sync Specify with local DB taxon names  
    # NOTE  Restricted to taxonnames where taxonid is NULL ('None')
    #       We're only looking at those taxa where the Sp7 foreign key is not set  
    print('*************************************************************')
    print('Checking Specify7 API for local db taxa with taxontree: %d' % taxontreedefid)
    for rank in taxonranks:
        rankid = rank['rankid']
        rankname = rank['name']
        if rankid > 10:
            print(' - For rank %s:"%s" ' %(rankid, rankname))
            dbTaxonNames = db.getRowsOnFilters('taxonname', {'rankid': '=%s' % rankid, 'taxontreedefid': '=%s' % taxontreedefid, 'taxonid' : 'IS NULL'})
            print(' - checking Specify7 API for %d rows from local DB for %s:"%s" ' % (len(dbTaxonNames), rankid, rankname))
            found = False
            for i in range(0, len(dbTaxonNames)):
                #id = dbTaxonNames[i]['taxonid']
                fullname = dbTaxonNames[i]['fullname']
                name = dbTaxonNames[i]['name']
                #print(' - checking Specify API for taxon:%s:"%s" ("%s")' %(id, fullname, name))
                spTaxonName = sp.fetchSpecifyObjects('taxon', csrftoken, 100,0,{"taxontreedefid":str(taxontreedefid), "rankid":str(rankid),"name":name,"fullname":fullname})
                if not spTaxonName:
                    print(' - taxon: "%s" ("%s") not found! ' %(fullname, name))
                    found = True
                    # TODO  Add missing taxon to Specify 
                    #       1. Insert taxon into Specify
                    #       2. Get newly inserted taxon's key (id) 
                    #       3. If rank lower than class, get newly inserted taxon's class foreign key 
                #if input('continue?') == 'n':break
            if not found:
                print(' - All rows accounted for...')
        #if input('continue?') == 'n':break

def updateSpecifyTaxonNames(taxonranks, taxontreedefid, csrftoken):
    # TODO Sync local database taxon names with those in Specify 
    pass
    


#def syncLocalTaxonHierarchyWithSpecify
    # TODO Sync taxononomic hierarchy table  
    
"""def getTaxonClass(taxonid, csrftoken):
    # TODO
    print(' - Retrieving class for taxon with id %s ...'%taxonid)
    
def getTaxonParent(taxonid, csrftoken):
    # TODO 
    print(' - Retrieving parent for taxon with id %s ...'%taxonid)
    taxon = sp.fetchSpecifyObject('taxon', taxonid, csrftoken)
    parent = sp.directAPIcall(taxon['parent'], csrftoken)
    return parent"""

# TEST CODE
util.clear()
print('------- Running specify_sync.py --------')
institution = db.getRowOnId('institution', 0)
# print(institution)
token = specifyLogin(institution[3], input('Enter username: '), getpass('Enter password: '))
if token != '':
    choice = input('Sync what? [1] collections [2] taxonomy ')
    #choice = "2"
    print('Your choice: "%s"' % choice)
    if choice == "1": syncSpecifyCollections(token)
    elif choice == "2": 
        syncTaxonomy(13, token, 15)
    else: print('You are the weakest link. Goodbye! ')
else:
    print('Login failed...')
print('----------- done --------------')



"""
specifyCollections = sp.getInitialCollections()
#sp.
localdbCollections = db.getRows('collection')

for key in specifyCollections:
    print('checking for collection {%s,%s} in db:' %(key, specifyCollections[key]))
    if(len(db.getRowsOnFilters('collection', {'spid': key, 'name' : '="%s"' % specifyCollections[key]}))> 0):
        print('found')
    else:
        print('not found')
    pass
"""
