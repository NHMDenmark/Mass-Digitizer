# -*- coding: utf-8 -*-
"""
  Created on August 17, 2022
  @author: Fedor Alexander Steeman, NHMD
  Copyright 2022 Natural History Museum of Denmark (NHMD)
  Licensed under the Apache License, Version 2.0 (the "License");
  you may not use this file except in compliance with the License.
  You may obtain a copy of the License at
  http://www.apache.org/licenses/LICENSE-2.0
  Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for the specific language governing permissions and limitations under the License.

  PURPOSE: Automate merging duplicates through the Specify API 
"""

from getpass import getpass
from models.model import Model

import specify_interface as sp
import global_settings as gs 

import models
from models import taxon
from models import collection as col

gs.baseURL = 'https://specify-test.science.ku.dk/'

def merge(source_target_tuple_list, spusername, sppassword, collection_id):
    # TODO function contract   
    # 

    token = sp.specifyLogin(spusername, sppassword, collection_id)
    if token == '': return 'Authentication error!'
    
    for duplicate in source_target_tuple_list: 
        source_taxon_id = duplicate[0]
        target_taxon_id = duplicate[1]
        print('merging %s with %s ...'%(source_taxon_id, target_taxon_id))
        print(sp.mergeTaxa(source_taxon_id, target_taxon_id, token))

def testcode():
    max_tries = 10
    while max_tries > 0:
        token = sp.specifyLogin(input('Enter username: '), getpass('Enter password: '), 688130)
        if token != '': break
        else:
            print('Login failed...')
            if input('Try again? (y/n)') == 'n': break
        max_tries = max_tries - 1
        print('Attempts left: %i' % max_tries)

    if token != '':
        source_taxon_id = input('enter source taxon id:')
        target_taxon_id = input('enter target taxon id:')

        sp.mergeTaxa(source_taxon_id, target_taxon_id, token)

    print('exiting...')

def main():

    max_tries = 10

    print('*** Specify Merge Duplicates ***')
    
    while max_tries > 0:
        print('Choose collection to scan: ')
        print('1. Vascular Plants (688130)')
        
        collectionId = 0
        collIndex = input('?')
        if collIndex == "1": 
            collectionId = 688130
        else: break 

        token = sp.specifyLogin(input('Enter username: '), getpass('Enter password: '), collectionId)

        # 
        collection = col.Collection(collectionId)
        collection.fill(sp.getSpecifyObject('collection', collectionId, token), token)

        print(f'Selection {collIndex}: {collection.spid}')
        if collection.spid > 0:
            if token != '': 
                max_tries = 0
                scan(collection, token)   
            else:
                print('Login failed...')
                if input('Try again? (y/n)') == 'n' : break
                max_tries = max_tries - 1
        else: 
            max_tries = max_tries - 1 
            print('Attempts left: %i' % max_tries)
    print('done')

def scan(collection, token):
    # 
    print(f'Scanning {collection.spid} ...')

    resultCount = -1    
    offset = 0

    # 
    taxonranks = sp.getSpecifyObjects('taxontreedefitem', token, 100, 0,
                                      {"treedef":str(collection.discipline.taxontreedefid)})

    print(len(taxonranks))

    # 
    for rank in taxonranks:
        
        rankId = int(rank['rankid'])
        print(f'RANK ID: {rankId}')
                
        # Only look at genera and below 
        if rankId >= 180:
            
            resultCount = -1
            while resultCount != 0:

                # Fetch batches from API
                print(f'Fetching batch with offset: {offset}')
                batch = sp.getSpecifyObjects('taxon', token, 100, offset, {'definition':'13', 'rankid':f'{rankId}'})
                resultCount = len(batch)

                print(f' - Fetched {resultCount} taxa')
                for b in batch:             
                    t = taxon.Taxon(collection.id)
                    t.fill(b)
                    #print(t)
                    fullName = t.fullname.replace(' ','%20')
                    taxonLookup = sp.getSpecifyObjects('taxon', token, 100000, 0, 
                        {'definition':'13', 'rankid':f'{rankId}', 'fullname':f'{fullName}'})

                    for tl in taxonLookup:
                        if tl['id'] != t.id:
                            print('Duplicate detected!')
                            
                            d = taxon.Taxon(collection.id)
                            d.fill(tl)

                            print(f' - original : "{t}"')
                            print(f' - duplicate : "{d}"')

                # Escape hatch
                if input('next batch (y/n)?') == 'n': 
                    resultCount = 0
                    break

                offset += 100
    
            # Escape hatch
            if input('next rank (y/n)?') == 'n': break

#testcode()

main()