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

  PURPOSE: Automate merging duplicates through the Specify API. 

  NOTE: For the time being this code is run directly from development environment using lines at the bottom of the file. 
        IMPORTANT! This is also where the target URL for the Specify7 API instance is set. 
"""

import sys
import time 
import logging
from getpass import getpass

#internal dependencies
import util
import specify_interface
import global_settings as gs 
import data_exporter
import GBIF_interface

from models.model import Model
from models import taxon
from models import collection as col
from models import discipline as dsc

class MergeDuplicates():

    def __init__(self) -> None:
        """
        Constructor for MergeDuplicates class. Sets up base global variables, instantiates utility classes and sets up logging. 
        """
        # Prepare variable base values  
        self.resultCount = -1    
        #self.offset = 0
        self.batchSize = 1000
        self.ambivalentCases = []

        self.sp = specify_interface.SpecifyInterface()
        self.gbif = GBIF_interface.GBIFInterface()
        self.dx = data_exporter.DataExporter()
        #db = data_access.DataAccess('db')

        # Set up logging
        self.logger = logging.getLogger('MergeDuplicates')
        self.logger.setLevel(logging.DEBUG)
        logFileFormatter = logging.Formatter(fmt=f"%(message)s", datefmt="%Y-%m-%d %H:%M:%S")
        fileHandler = logging.FileHandler(filename=f'log/MergeDuplicates_{time.time()}.log')
        fileHandler.setFormatter(logFileFormatter)
        fileHandler.setLevel(level=logging.INFO)
        self.logger.addHandler(fileHandler)

    def main(self):
        """
        Main method for class allowing for user interaction via Command Line Interface. 
        After choosing collection, user is logged in to the Specify7 API and the merging proceeds through two different methods: 
        1. By going through list of precollected taxon ids stored in file 'bootstrap/duplicate-taxa-ids.txt' (checkPrecollectedTaxa)
        2. By going through all taxa from top to bottom checking for each whether there is a possible duplicate
        """

        max_tries = 10 # maximum number of attempts to log in. Is decremented upon every log in failure. 

        self.logger.info('*** Specify Merge Duplicates ***')
        
        while max_tries > 0:
            self.logger.info('Choose collection to scan: ')
            self.logger.info('1. Vascular Plants (688130)')
            
            # Allow user selection of collection (currently limited to NHMD Vascular Plants)
            collectionId = 0
            collIndex = input('?')
            if collIndex == "1": 
                # NHMD Vascular plants selected  
                collectionId = 688130
            else: break 

            # Get username and password from input and log in to Specify7 API 
            token = self.sp.specifyLogin(input('Enter username: '), getpass('Enter password: '), collectionId)
            # Upon succesful login, valid token is produced 

            if token != '': 
                # User is succesfully logged into Specify7 API: Proceed to fetch collection & discipline data and instantiate corresponding model objects. 
                self.collection = col.Collection(collectionId)
                spCollection = self.sp.getSpecifyObject('collection', collectionId)
                self.collection.fill(spCollection)
                spDiscipline = self.sp.getSpecifyObject('discipline', self.collection.disciplineId)
                self.collection.discipline = dsc.Discipline(self.collection.collectionId)
                self.collection.discipline.fill(spDiscipline)
                
                self.logger.info(f'Selection {collIndex}: {self.collection.spid}')
                
                if self.collection.spid > 0:
                    # Collection object succesfully fetched & instantiated  
                    max_tries = 0
                    #self.handleQualifiedTaxa()
                    self.checkPrecollectedTaxa()
                    self.scan()
                else: 
                    # Login failed: Allow user another attempt out of the decremented maximum number of tries 
                    self.logger.info('Login failed...')
                    max_tries = max_tries - 1
                    self.logger.info('Attempts left: %i' % max_tries)
                    if input('Try again? (y/n)') == 'n' : break
            else:
                # Login failed: Allow user another attempt out of the decremented maximum number of tries 
                self.logger.info('Login failed...')
                max_tries = max_tries - 1
                self.logger.info('Attempts left: %i' % max_tries)
                if input('Try again? (y/n)') == 'n' : break
                
        self.logger.info('done')

    def checkPrecollectedTaxa(self):
        """
        Function for going through list of collection taxon ids that are likely to have duplicates to be merged.  
        The list is retrieved from a simple text file with a taxon id for each line. 
        The text file itself is based on the results of a query joining taxa on fullname (GetTaxonDuplicates.sql in 'sql' folder). 
        """
        idList = open('bootstrap/duplicate-taxa-ids.txt', 'r')
        taxonIds = idList.readlines() 
        print(f'Checking {len(taxonIds)} pre-collected taxa...')
        for taxonId in taxonIds: 
            taxonId = int(taxonId)
            #print(f'Fetching taxon with id: {taxonId}')
            specifyTaxon = self.sp.getSpecifyObject('taxon', int(taxonId))
            if specifyTaxon:
                # If 
                self.handleSpecifyTaxon(specifyTaxon)
            else:
                print(f'Could not retrieve taxon...', end='') 

    def scan(self):
        """
        Function for scanning and iterating taxa retrieved from the Specify API in batches per taxon rank.         """
        
        self.logger.info(f'Scanning {self.collection.spid} ...')

        # Fetch taxon ranks from selected collection's discipline taxon tree 
        taxonranks = self.sp.getSpecifyObjects('taxontreedefitem', 100, 0, {"treedef":str(self.collection.discipline.taxontreedefid)})

        # Iterate taxon ranks for analysis
        for rank in taxonranks:
            # Extract rank id & display 
            rankId = int(rank['rankid'])
            rankName = str(rank['name'])
            self.logger.info(f'RANK "{rankName}" ({rankId})')
                    
            # Only look at rank genera and below 
            if rankId >= 181:
                offset = 0
                resultCount = -1
                while resultCount != 0:

                    # Fetch batches from API
                    self.logger.info(f'Fetching batch with offset: {offset}')
                    batch = self.sp.getSpecifyObjects('taxon', self.batchSize, offset, {'definition':'13', 'rankid':f'{rankId}'})
                    resultCount = len(batch)

                    self.logger.info(f' - Fetched {resultCount} taxa')

                    # Iterate taxa in batch 
                    for specifyTaxon in batch:
                        self.handleSpecifyTaxon(specifyTaxon)
                    print()
                    
                    # Prepare for fetching next batch, by increasing offset with batchsize 
                    offset += self.batchSize
        
        # Handle Ambivalent cases: Save & export to file 
        self.logger.info('Handle ambivalent cases...')
        for case in self.ambivalentCases: 
            self.logger.info(f' - {case}')
            case.save()
        self.logger.info(self.dx.exportTable('taxon', 'xlsx'))

    def handleSpecifyTaxon(self, specifyTaxon):
        """
        Handle Specify taxon json object through the following steps: 
          - Create taxon model object instance
          - Look up possible duplicates at Specify7 API 
          - Performing merge of any unambiguous duplicates after updating author info if needed 
          - Recording any ambivalent cases
        """
        print('.', end='')  
        # Create local taxon instance from original Specify taxon data 
        original = taxon.Taxon(self.collection.id)
        original.fill(specifyTaxon)
        #original.parent.fill(self.sp.getSpecifyObject(original.sptype, original.parentId))
        original.getParent(self.sp)
        fullName = original.fullName.replace(' ','%20')
        rankId = original.rankId

        # Look up taxa with matching fullname & rank
        taxonLookup = self.sp.getSpecifyObjects('taxon', 100000, 0, 
            {'definition':'13', 'rankid':f'{rankId}', 'fullname':f'{fullName}'}) #, 'parent':f'{original.parentid}'})
        
        # If more than one result is returned, there will be duplicates 
        if len(taxonLookup) > 1:
            
            # Iterate taxa with identical names to original                             
            for tl in taxonLookup:
                # Create local taxon instance from looked up Specify taxon data 
                lookup = taxon.Taxon(self.collection.id)
                lookup.fill(tl)
                #lookup.parent.fill(self.sp.getSpecifyObject(lookup.sptype, lookup.parentId))
                lookup.getParent(self.sp)

                # If the looked up taxon isn't the same record (as per 'spid') then treat as potential duplicate 
                # NOTE We need to compare the Specify id ('spid') and not the local id, which is always 0 until saved
                if lookup.spid != original.spid:

                    # If the parents match then treat as duplicate 
                    if lookup.parentId == original.parentId:
                        print()
                        self.logger.info('Duplicate detected!')
                        self.logger.info(f' - original : "{original}"')
                        self.logger.info(f' - duplicate : "{lookup}"')
                        
                        # Reset variables for weighting the two candidates for merging 
                        originalWeight  = 0
                        duplicateWeight = 0

                        # If original author is empty, but lookup author isn't, then weight lookup higher
                        if original.author == None and lookup.author is not None: 
                            duplicateWeight += 1
                        # TODO more weighting rules ? 
                        
                        # If both original and lookup contain author data and the author is not identical, 
                        #   retrieve authorship from GBIF 
                        unResolved = True 
                        if (original.author != lookup.author) and (original.author is not None or lookup.author is not None) and (original.author != '' or lookup.author != ''): # and (original.author is not None and lookup.author is not None): 
                            #self.logger.info('Both original and lookup contain author data and the author is not identical! ')
                            self.logger.info('Original author and lookup author are not identical and neither is empty!')
                            self.logger.info('Retrieving authorship from GBIF...')
                            
                            criterium1 = self.resolveAuthorName(original)
                            criterium2 = self.resolveAuthorName(lookup)
                            unResolved = criterium1 and criterium2 
                        else:
                            if (original.author is None and lookup.author is None):
                                self.logger.info('Author info is missing...')
                                # Update authorname at Specify also 
                                criterium1 = self.resolveAuthorName(original)
                                criterium2 = self.resolveAuthorName(lookup)
                                unResolved = criterium1 and criterium2
                            else:
                                self.logger.info('Original and lookup have no author data or the author is identical. ')
                                unResolved = False  

                        if unResolved:
                        # If authorship could not be resolved, add to ambivalent cases 
                            ambivalence = f'Ambivalence on authors: {original.author} vs {lookup.author} '
                            self.logger.info(ambivalence)
                            original.remarks = str(original.remarks) + f' | {ambivalence}'
                            original.duplicateSpid = lookup.spid
                            self.ambivalentCases.append(original)
                            lookup.remarks = str(lookup.remarks) + f' | {ambivalence}'
                            lookup.duplicateSpid = original.spid
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
                                # Stop latch for user interaction (disabled)
                                if True: # input(f'Do you want to merge {source.spid} with {target.spid} (y/n)?') == 'y':
                                    # Do the actual merging 
                                    start = time.time()
                                    response = self.sp.mergeTaxa(source.spid, target.spid)
                                    if response.status_code == "404":
                                        self.logger.info(' - 404: Taxon already merged.')
                                    elif response.status_code == "500":
                                        self.logger.info(' - 500: Internal Server Error.')
                                    end = time.time()
                                    timeElapsed = end - start
                                    self.logger.info(f'Merged {source.spid} with {target.spid}; Time elapsed: {timeElapsed} ')
                                    pass
                    else:
                        # Found taxa with matching names, but different parents: Add to ambivalent cases 
                        ambivalence = f'Ambivalence on parent taxa: {original.parent.fullName} vs {lookup.parent.fullName} '
                        self.logger.info(ambivalence)
                        original.remarks = str(original.remarks) + f' | {ambivalence}'
                        original.duplicateSpid = lookup.spid
                        self.ambivalentCases.append(original)
                        lookup.remarks = str(lookup.remarks) + f' | {ambivalence}'
                        lookup.duplicateSpid = original.spid
                        self.ambivalentCases.append(lookup)
        else:
            print('x', end='')

    def resolveAuthorName(self, taxonInstance):
        """
        Method for resolve the author name of a given taxon class instance by consulting the GBIF API 
        CONTRACT 
            taxonInstance (taxon.Taxon) : Taxon class instance for which the author should be resolved
        RETURNS boolean : Flag to indicate whether the resolution was succesful 
        """
        self.logger.info('Resolving author name...')
        acceptedNameMatches = self.gbif.matchName('species', taxonInstance.fullName, self.collection.spid)
                            
        nrOfMatches = len(acceptedNameMatches)
        if nrOfMatches == 1:
            self.logger.info('Retrieved unambiguous accepted name from GBIF...')
            # Update the authorname at Specify 
            res = self.updateSpecifyTaxonAuthor(taxonInstance, acceptedNameMatches[0]['authorship'])
            if res != '500':
                unResolved = False
            else:
                unResolved = True
        else:
            self.logger.info(f'Could not retrieve unambiguous accepted name from GBIF... ({nrOfMatches} matches)')
            unResolved = True
        return unResolved

    def updateSpecifyTaxonAuthor(self, taxonInstance, acceptedAuthor):
        """
        Function for direct call to Specify7 API to set a new author name. 
        """
        # Update the authorname at Specify 
        self.logger.info(f'Updating author name at Specify for: [{taxonInstance}] to: "{acceptedAuthor}"')
        spobjOriginal = self.sp.getSpecifyObject('taxon',taxonInstance.spid)
        if spobjOriginal: 
            spobjOriginal['author'] = acceptedAuthor
            return self.sp.putSpecifyObject('taxon', taxonInstance.spid, spobjOriginal)
        else: 
            return 500 

    def recordAmbivalentCase(self, original, lookup, ambivalence):
        """
        Function for recording ambivalent duplicate cases for export 
        """
        # 
        self.logger.info(ambivalence)
        original.remarks = str(original.remarks) + f' | {ambivalence}'
        self.ambivalentCases.append(original)
        lookup.remarks = str(lookup.remarks) + f' | {ambivalence}'
        self.ambivalentCases.append(lookup)


gs.baseURL = 'https://specify-snm.science.ku.dk/' # Set target URL for Specify7 API instance 

md = MergeDuplicates() # Instantiate class 

md.main() # Run code 

