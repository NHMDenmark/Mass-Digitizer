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

import util
import specify_interface
import global_settings as gs 
import data_exporter as dx
from models.model import Model
from models import taxon
from models import collection as col

gs.baseURL = 'https://specify-test.science.ku.dk/'

sp = specify_interface.SpecifyInterface()

class MergeDuplicates():

    def __init__(self) -> None:
        
        # Prepare variable base values  
        self.resultCount = -1    
        self.offset = 0
        self.batchSize = 1000
        self.ambivalentCases = []

    def main(self):

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
                    self.scan(collection, token)   
                else:
                    print('Login failed...')
                    if input('Try again? (y/n)') == 'n' : break
                    max_tries = max_tries - 1
            else: 
                max_tries = max_tries - 1 
                print('Attempts left: %i' % max_tries)
        print('done')

    def scan(self, collection, token):
        # function for scanning and iterating taxa retrieved from the Specify API in batches per taxon rank 
        print(f'Scanning {collection.spid} ...')

        # Fetch taxon ranks from selected collection's discipline taxon tree 
        taxonranks = sp.getSpecifyObjects('taxontreedefitem', token, 100, 0,
                                        {"treedef":str(collection.discipline.taxontreedefid)})

        # Iterate taxon ranks for analysis
        for rank in taxonranks:
            # Extract rank id & display 
            rankId = int(rank['rankid'])
            rankName = str(rank['name'])
            print(f'RANK "{rankName}" ({rankId})')
                    
            # Only look at rank genera and below 
            if rankId >= 180:
                offset = 0
                resultCount = -1
                while resultCount != 0:

                    # Fetch batches from API
                    print(f'Fetching batch with offset: {offset}')
                    batch = sp.getSpecifyObjects('taxon', token, self.batchSize, offset, {'definition':'13', 'rankid':f'{rankId}'})
                    resultCount = len(batch)

                    print(f' - Fetched {resultCount} taxa')

                    # Iterate taxa in batch 
                    for specifyTaxon in batch:
                        print('.', end='')  

                        # Create local taxon instance from original Specify taxon data 
                        original = taxon.Taxon(collection.id)
                        original.fill(specifyTaxon)
                        original.getParent(token)
                        fullName = original.fullname.replace(' ','%20')

                        # Look up taxa with matching fullname & rank
                        taxonLookup = sp.getSpecifyObjects('taxon', token, 100000, 0, 
                            {'definition':'13', 'rankid':f'{rankId}', 'fullname':f'{fullName}'}) #, 'parent':f'{original.parentid}'})
                        
                        # If more than one result is returned, there will be duplicates 
                        if len(taxonLookup) > 1:
                            
                            # Iterate taxa with identical names to original                             
                            for tl in taxonLookup:
                                # Create local taxon instance from looked up Specify taxon data 
                                lookup = taxon.Taxon(collection.id)
                                lookup.fill(tl)
                                lookup.getParent(token)

                                # If the looked up taxon isn't the same record (as per 'spid') then treat as potential duplicate 
                                # NOTE We need to compare the Specify id ('spid') and not the local id, which is always 0 until saved
                                if lookup.spid != original.spid:

                                    # If the parents match then treat as duplicate 
                                    if lookup.parentid == original.parentid:
                                        print()
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
                                        #   except when the author is identical 
                                        if (original.author is not None and lookup.author is not None) and (original.author != lookup.author): 
                                            ambivalence = f'Ambivalence on authors: {original.author} vs {lookup.author} '
                                            print(ambivalence)
                                            original.remarks = str(original.remarks) + f' | {ambivalence}'
                                            original.duplicatespid = lookup.spid
                                            self.ambivalentCases.append(original)
                                            lookup.remarks = str(lookup.remarks) + f' | {ambivalence}'
                                            lookup.duplicatespid = original.spid
                                            self.ambivalentCases.append(lookup)
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
                                                if True: #input(f'Do you want to merge {source.spid} with {target.spid} (y/n)?') == 'y':
                                                    # Do the actual merging 
                                                    start = time.time()
                                                    response = sp.mergeTaxa(source.spid, target.spid, token)
                                                    if response.status_code == "404":
                                                        print(' - 404: Taxon already merged.')
                                                    end = time.time()
                                                    timeElapsed = end - start
                                                    print(f'Merged {source.spid} with {target.spid}; Time elapsed: {timeElapsed} ')
                                    else:
                                        # Found taxa with matching names, but different parents: Add to ambivalent cases 
                                        ambivalence = f'Ambivalence on parent taxa: {original.parent.fullname} vs {lookup.parent.fullname} '


                    # Escape hatch
                    #print()
                    #if input('next batch (y/n)?') == 'n': 
                    #    resultCount = 0
                    #    break
                    print()
                    
                    # Prepare for fetching next batch, by increasing offset with batchsize 
                    offset += self.batchSize
        
                # Escape hatch
                #print()
                #if input('next rank (y/n)?') == 'n': break
        
        # Handle Ambivalent cases: Save & export to file 
        print('Handle ambivalent cases...')
        for case in self.ambivalentCases: 
            print(' - ', case)
            case.save()
        print(dx.exportTable('taxon', 'xlsx'))

    def recordAmbivalentCase(self, original, lookup, ambivalence):
        print(ambivalence)
        original.remarks = str(original.remarks) + f' | {ambivalence}'
        ambivalentCases.append(original)
        lookup.remarks = str(lookup.remarks) + f' | {ambivalence}'
        ambivalentCases.append(lookup)

md = MergeDuplicates()
md.main()