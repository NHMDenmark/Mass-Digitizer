# -*- coding: utf-8 -*-
"""
  Created on December 18, 2023
  @author: Fedor Alexander Steeman, NHMD
  Copyright 2023 Natural History Museum of Denmark (NHMD)
  Licensed under the Apache License, Version 2.0 (the "License");
  you may not use this file except in compliance with the License.
  You may obtain a copy of the License at
  http://www.apache.org/licenses/LICENSE-2.0
  Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for the specific language governing permissions and limitations under the License.

  PURPOSE: 
  Prepares a fresh database filled with predefined data to be bundled with the MassDigitizer App.
"""

from pathlib import Path
import csv
import time
import sqlite3

# Local imports
import data_access

class PrepareDatabase():
    """
    Creates and prepares a fresh database filled with predefined data to be bundled with the MassDigitizer App.
    """

    def main(self):
        """
        Main function to create and prepare the fresh database.
        """
       
        db_file = self.create_database(Path(r'MassDigitizer\db'))

        # Populate tables with predefined data
        self.populate_predefined_tables(Path(db_file))

        # Populate taxonname table from taxon spine files
        self.populate_taxonname_table(Path(r'MassDigitizer\db\db.sqlite3'))

        # Run optimizations
        self.run_optimizations(Path(db_file))

    def create_database(self, file_path):
        """
        Creates a fresh skeleton database at the provided path.
        Deletes any preexisting database file at that path.
        """

        db_file = file_path / 'db.sqlite3'
        sql_file = file_path / 'create_db.sqlite3.sql'

        #Remove existing database file if it exists
        if Path(db_file).exists(): Path(db_file).unlink()

        #Create new database 
        with sqlite3.connect(db_file) as conn:
            with open(sql_file, 'r', encoding='utf-8') as sql_file:
                sql_script = sql_file.read()
                conn.executescript(sql_script)
        
        return db_file
        
    def populate_predefined_tables(self,db_file_path):
        """
        Populates predefined tables in the database located at the provided path.
        """

        db = data_access.DataAccess('db', db_file_path)

        # Define editions and SQL files
        editions = [r'NHMD\tracheophyta', r'NHMD\entomology', r'NHMA\entomology']
        sqlfiles = [r'PrepTypes', r'TypeStatuses', r'GeoRegions', r'Storage', r'Highertaxa', r'Species-Batch1', r'Species-Batch2', r'Species-Batch3', r'Species-Batch4', r'Subspecies', r'VarForma-Batch1', r'VarForma-Batch2', r'Hybrids']

        for edition in editions:
            for sqlfile in sqlfiles:
                sql_file_path = Path(r'MassDigitizer\sql\editions') / edition / f'{sqlfile}.sql'
                print(f'Populating from file: {str(sql_file_path)}')
                sql_file = open(sql_file_path, 'r', encoding="utf-8")
                sql_statement = sql_file.read()
                sql_file.close()
                db.executeSqlStatement(sql_statement)

    def populate_taxonname_table(self, db_file_path):
        """
        Populates the taxonname table in the database located at the provided path.
        """

        filePairs = self.get_filepairs()

        db = data_access.DataAccess(db_file_path)

        for filePair in filePairs:

            sourceFile = filePair['source']
            print('**************')
            print(sourceFile)
            tsv_file = open(sourceFile, 'r', encoding="utf-8")
            tsv_reader = csv.DictReader(tsv_file, delimiter='\t')
            
            sql_statement = "INSERT INTO taxonname (spid, dwcid,dasscoid,name,author,fullname,rankid,taxonrank,parentfullname,acceptedfullname,treedefid,idnumber,taxonnrsource) VALUES \n" 

            print('* generating sql *')
            t1 = time.time()
            for line in tsv_reader:
                sql_statement = sql_statement + self.generateValuesClause(line, 13) + ', \n'
            sql_statement = sql_statement[:-3] + ';'            
            t2 = time.time() - t1
            print(f'time spent: {str(t2)}' )        
            
            fileWriter = open(filePair['destin'], "w", encoding='utf-8')
            fileWriter.write(sql_statement)
            fileWriter.close()

            print('* executing sql *')
            t1 = time.time()
            db.executeSqlStatement(sql_statement)
            t2 = time.time() - t1
            print(f'time spent: {str(t2)}' )
    
    def run_optimizations(self, db_file_path):
        """
        Runs optimizations on the database located at the provided path.
        """

        db = data_access.DataAccess('db', db_file_path)
        optimization_sql_file = Path(r'MassDigitizer\sql\optimizations.sql')
        print(f'Running optimizations from file: {str(optimization_sql_file)}')
        sql_file = open(optimization_sql_file, 'r', encoding='utf-8')
        sql_script = sql_file.read()
        sql_file.close()
        db.executeSqlStatement(sql_script) 

    def get_filepairs(self):
        """
        Returns a list of dictionaries containing source and destination file paths for taxon spine files.
        """        

        return [{'source' : r'data\taxon spines\Botany\Tracheophyta 01 higher taxa.tsv', 
              'destin' : r'MassDigitizer\sql\editions\NHMD\tracheophyta\Highertaxa.sql'},

             {'source' : r'data\taxon spines\\Botany\Tracheophyta 02 species accepted.tsv', 
              'destin' : r'MassDigitizer\sql\editions\NHMD\tracheophyta\Species-Batch1.sql'},

             {'source' : r'data\taxon spines\\Botany\Tracheophyta 02 species synonyms part1.tsv', 
              'destin' : r'MassDigitizer\sql\editions\NHMD\tracheophyta\Species-Batch2.sql'},

             {'source' : r'data\taxon spines\\Botany\Tracheophyta 02 species synonyms part2.tsv', 
              'destin' : r'MassDigitizer\sql\editions\NHMD\tracheophyta\Species-Batch3.sql'}, 

             {'source' : r'data\taxon spines\\Botany\Tracheophyta 03 subspecies.tsv', 
              'destin' : r'MassDigitizer\sql\editions\NHMD\tracheophyta\Subspecies.sql'}, 

             {'source' : r'data\taxon spines\\Botany\Tracheophyta 04 infraspecific accepted.tsv', 
              'destin' : r'MassDigitizer\sql\editions\NHMD\tracheophyta\VarForma-Batch1.sql'}, 

             {'source' : r'data\taxon spines\\Botany\Tracheophyta 04 infraspecific synonyms.tsv', 
              'destin' : r'MassDigitizer\sql\editions\NHMD\tracheophyta\VarForma-Batch2.sql'}, 

             {'source' : r'data\taxon spines\\Botany\Tracheophyta 05 hybrids.tsv', 
              'destin' : r'MassDigitizer\sql\editions\NHMD\tracheophyta\Hybrids.sql'}
            ]

    def generateValuesClause(self, line, treedefid):
        """
        TODO
        """

        sp_taxonID          = line['sp:taxonID'] or 0
        dwc_taxonID         = line['dwc:taxonID'] or 0
        author              = line['dassco:author']
        dassco_taxonID      = line['dassco:taxonID']
        dassco_name         = line['dassco:name']
        dassco_fullname     = line['dassco:fullname'] 
        dassco_rankid       = line['dassco:rankid'] or 0
        dwc_taxonRank       = line['dwc:taxonRank']
        dwc_parentNameUsage = line['dwc:parentNameUsage']
        sp_taxonRank        = line['sp:rankname']
        sp_parentname       = line['sp:parentname']
        acceptedfullname    = line['dwc:acceptedNameUsage']
        sp_taxonnr          = line['sp:taxonnr']
        sp_taxonnrsource    = line['sp:taxonnrsource']

        # The main values are: spid, dwcid, dasscoid, name (dassco), author (dassco), fullname (dassco), rankid (dassco) 
        values_main   = f'({sp_taxonID},{dwc_taxonID},"{dassco_taxonID}","{dassco_name}","{author}","{dassco_fullname}",{dassco_rankid},'

        values_sp_dwc = "'','',''," # Values predicated on dwc:taxonID or sp:taxonID respectively
                                 # These correspond to: taxonrank, parentfullname, acceptedfullname 
        if line['dwc:taxonID']:
            values_sp_dwc = f'"{dwc_taxonRank}","{dwc_parentNameUsage}","{acceptedfullname}",' 
        else:
            if line['sp:taxonID']:
                values_sp_dwc = f'"{sp_taxonRank}","{sp_parentname}","",' # NOTE No accepted names from Specify (yet)

        # Specify-specific values are: tree definition primary key, taxon number and its source (checklist or similar) 
        values_sponly = f'{treedefid},"{sp_taxonnr}","{sp_taxonnrsource}")'

        # Combined clause is returned 
        return values_main + values_sp_dwc + values_sponly  

# 
PrepareDatabase().main()
