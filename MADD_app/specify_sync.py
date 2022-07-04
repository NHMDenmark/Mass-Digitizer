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
    # TODO
    print('Connecting to Specify7 API...')
    sp.initInstitution(baseURL)
    csrftoken = sp.getCSRFToken()
    csrftoken = sp.login(username, passwd, csrftoken)
    if sp.verifySession(csrftoken):
        return csrftoken
    else:
        return '' 

def specifyLogout(csrftoken):
    # TODO
    print('logging out of Specify...')
    sp.logout(csrftoken)

def syncSpecifyCollections(csrftoken):
    # TODO
    print('Syncing collections with Specify...')
    specifyCollections = sp.fetchSpecifyObjects('collection', csrftoken)    
    for i in range(0, len(specifyCollections)):
        spCollection = specifyCollections[i]
        print(' - checking db for collection {%s,"%s"} ...' %(spCollection['id'], spCollection['collectionname']))
        dbCollection = db.getRowsOnFilters('collection', {'spid': spCollection['id']})
        if len(dbCollection)==0:
            discipline = sp.directAPIcall(spCollection["discipline"], csrftoken)
            fields = {"spid" : spCollection["id"],"name" : '"%s"' % spCollection["collectionname"],"institutionid" : institution[0],"taxontreedefid" : discipline["taxontreedef"].split(r'/')[4]}
            print(db.insertRow('collection', fields))

def syncTaxonNames(taxontreedefid, csrftoken, limit=10):
    # TODO 
    print('Syncing taxonnames with Specify...')
    # First get available ranks for taxon tree in question
    taxonranks = sp.fetchSpecifyObjects('taxontreedefitem', csrftoken, limit, 0,{"treedef":str(taxontreedefid)})
    
    # 1. Sync database with specify taxa 
    print(' - Checking local database for Specify taxa with taxontree: %d' % taxontreedefid)
    # Loop through each rank, checking whether local db has an entry for this taxon 
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
                dbTaxonName = db.getRowsOnFilters('taxonname', {'fullname':'"%s"' % fullname, 'taxonid':'%s' % id}) # TODO filter on taxontreedefid !!! 
                #print(' - found %d rows for %s:"%s" ' % (len(dbTaxonNames), id, fullname))
                #print(dbTaxonNames)
                if len(dbTaxonName)==0: 
                    print(' - %s:"%s" ("%s") not in DB ' %(id, fullname, name))

    # 2. Next: Sync specify with database taxa 
    # NOTE restrict to taxonnames with taxonid = NULL ? 
    print(' - Checking Specify API for local db taxa with taxontree: %d' % taxontreedefid)
    for rank in taxonranks:
        rankid = rank['rankid']
        rankname = rank['name']
        if rankid > 10:
            print(' - For rank %s:"%s" ' %(rankid, rankname))
            dbTaxonNames = db.getRowsOnFilters('taxonname', {'rankid': '%s' % rankid, 'taxontreedefid': '%s' % taxontreedefid})
            print(' - found %d rows for %s:"%s" ' % (len(dbTaxonNames), rankid, rankname))
            for i in range(0, len(dbTaxonNames)):
                id = dbTaxonNames[i]['taxonid']
                fullname = dbTaxonNames[i]['fullname']
                name = dbTaxonNames[i]['name']
                #print(' - checking Specify API for taxon:%s:"%s" ("%s")' %(id, fullname, name))
                spTaxonName = sp.fetchSpecifyObjects('taxon', csrftoken, 100,0,{"id":str(id), "rankid":str(rankid),"name":name,"fullname":fullname})
                if not spTaxonName:
                    print(' - taxon taxon:%s:"%s" ("%s") not found! ' %(id, fullname, name))
                #if input('continue?') == 'n':break
        if input('continue?') == 'n':break
    



    

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
token = specifyLogin(institution[3], 'test', 'testytest') #input('Enter username: '), getpass('Enter password: '))
if token != '':
    #choice = input('Sync what? [1] collections [2] taxonnames ')
    choice = "2"
    print('Your choice: "%s"' % choice)
    if choice == "1": syncSpecifyCollections(token)
    elif choice == "2": 
        syncTaxonNames(13, token, 15)
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
    if(len(db.getRowsOnFilters('collection', {'spid': key, 'name' : '"%s"' % specifyCollections[key]}))> 0):
        print('found')
    else:
        print('not found')
    pass
"""









