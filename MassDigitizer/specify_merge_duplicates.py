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

import time 
from getpass import getpass

import specify_interface as sp
import global_settings as gs 
from models.model import Model
from models import taxon
from models import collection as col

gs.baseURL = 'https://specify-test.science.ku.dk/'

def main():

    max_tries = 10

    print('*** Specify Merge Duplicates ***')
    
    while max_tries > 0:
        print('Choose collection to scan: ')
        print('1. Vascular Plants (688130)')
        
        collectionId = 0
        collIndex = "1" #input('?')
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
    limit = 100
    ambivalentCases = {}

    # 
    taxonranks = sp.getSpecifyObjects('taxontreedefitem', token, 100, 0,
                                      {"treedef":str(collection.discipline.taxontreedefid)})

    print(len(taxonranks))

    # 
    for rank in taxonranks:
        
        rankId = int(rank['rankid'])
        print(f'RANK ID: {rankId}')
                
        # Only look at genera and below 
        if rankId >= 220:
            offset = 0
            resultCount = -1
            while resultCount != 0:

                # Fetch batches from API
                print(f'Fetching batch with offset: {offset}')
                batch = sp.getSpecifyObjects('taxon', token, limit, offset, {'definition':'13', 'rankid':f'{rankId}'})
                resultCount = len(batch)

                print(f' - Fetched {resultCount} taxa')
                for b in batch:
                    print('.', end='')             
                    original = taxon.Taxon(collection.id)
                    original.fill(b)
                    #print(original)
                    fullName = original.fullname.replace(' ','%20')

                    # Look up taxa with matching fullname & rank
                    taxonLookup = sp.getSpecifyObjects('taxon', token, 100000, 0, 
                        {'definition':'13', 'rankid':f'{rankId}', 'fullname':f'{fullName}'}) #, 'parent':f'{original.parentid}'})

                    for tl in taxonLookup:
                        # Iterate taxon with 
                        lookup = taxon.Taxon(collection.id)
                        lookup.fill(tl)

                        # If the looked up taxon isn't the same record (as per 'id') then treat as potential duplicate 
                        if lookup.id != original.id:

                            # If the parents match then treat as duplicate 
                            if lookup.parentid == original.parentid:
                                print('Duplicate detected!')
                                print(f' - original : "{original}"')
                                print(f' - duplicate : "{lookup}"')
                                
                                # Reset variables for weighting the two candidates for merging 
                                originalWeight  = 0
                                duplicateWeight = 0

                                # If original author is empty, but lookup author isn't, then weight lookup higher
                                if original.author == None and lookup.author is not None: 
                                    duplicateWeight += 1
                                # TODO more weighting rules ? 
                                
                                # If both original and lookup contain author data: Add to ambivalent cases 
                                if original.author is not None and lookup.author is not None: 
                                    # TODO double check 
                                    original.remarks += ' | Ambivalent duplicate | '
                                    ambivalentCases.append(original)
                                    lookup.remarks += ' | Ambivalent duplicate | '
                                    ambivalentCases.append(lookup)
                                else: 
                                    # Prepare for merging by resetting target & source before evaluation 
                                    target = None
                                    source = None
                                    # Determine target and source taxon record as based on weighting 
                                    if duplicateWeight > originalWeight: 
                                        # Prefer looked up duplicate over original 
                                        target = lookup
                                        source = original 
                                    else: 
                                        # Prefer original 
                                        target = original
                                        source = lookup 

                                    # Merge taxa 
                                    if target is not None and source is not None: 
                                        # Stop latch for user interaction 
                                        if input(f'Do you want to merge {source.id} with {target.id} (y/n)?') == 'y':
                                            # Do the actual merging 
                                            start = time.time()
                                            sp.mergeTaxa(source.id, target.id, token)
                                            end = time.time()
                                            timeElapsed = end - start
                                            print(f'Merged {source.id} with {target.id}; Time elapsed: {timeElapsed} ')
                            else:
                                # Found taxa with matching names, but different parents: Add to ambivalent cases 
                                # TODO double check 
                                original.remarks += ' | Ambivalent duplicate | '
                                ambivalentCases.append(original)
                                lookup.remarks += ' | Ambivalent duplicate | '
                                ambivalentCases.append(lookup)

                # Escape hatch
                # if input('next batch (y/n)?') == 'n': 
                #     resultCount = 0
                #     break
                print()

                offset += limit
    
            # Escape hatch
            print()
            if input('next rank (y/n)?') == 'n': break
    
    # Handle Ambivalent cases 
    print('Handle ambivalent cases...')
    for case in ambivalentCases: 
        print(' - ', case)
        #case.save()



main()