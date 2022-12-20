# -*- coding: utf-8 -*-
"""
  Created on 2022-09-22
  @author: Fedor Alexander Steeman, NHMD
  Copyright 2022 Natural History Museum of Denmark (NHMD)
  Licensed under the Apache License, Version 2.0 (the "License");
  you may not use this file except in compliance with the License.
  You may obtain a copy of the License at
  http://www.apache.org/licenses/LICENSE-2.0
  Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for the specific language governing permissions and limitations under the License.

  PURPOSE: Exporting data from local database 
"""

import os
import pandas as pd
import tempfile as tf
from datetime import datetime as dt

# internal dependencies
import data_access
import global_settings as gs

db = data_access.DataAccess(gs.databaseName)

exportableTables = {'specimen', 'taxon'}

filePath = os.path.expanduser(r'~\Documents\DaSSCO') # In order to debug / run, a copy of the db file should be moved into this folder on Windows machines
altFilePath = os.path.expanduser(r'~\OneDrive - University of Copenhagen\Documents\DaSSCO\db.sqlite3') # For OneDrive users this is the file location

class DataExporter():

  def __init__(self):
        """
        Initialize Data Exporter  
        """

  def exportSpecimens(self, file_type):
    """
    Overloading of function exportTable specific for specimen data records 
    CONTRACT 
       file_type (String): Extension of the file type to be exported to 
           NOTE Only "xlsx" is currently supported 
       RETURNS Text string showing results of the export. In case of success, the path and filename. 
    """
    return self.exportTable('specimen', file_type)

  def exportTable(self, table_name, file_type):
    """
    Export records from table as specified into file of type specified (currently only xlsx is supported)
    CONTRACT 
       table_name (String): The name of the table to be exported from 
       file_type (String): Extension of the file type to be exported to 
           NOTE Only "xlsx" is currently supported 
       RETURNS Text string showing results of the export. In case of success, the path and filename. 
    """
    if table_name in exportableTables:
      sqlString = f'SELECT * FROM {table_name} WHERE exported = 0 OR exported IS NULL;'
      
      data_frame = pd.read_sql_query(sqlString, db.getConnection())

      if data_frame.__len__() < 1: 
        return 'No %s records to export.'%table_name

      try:
        file_name = self.generateFilename(table_name,file_type, filePath)
      except:
        file_name = self.generateFilename(table_name,file_type, altFilePath)
      data_frame.to_excel(file_name)

      pk_list = self.getPrimaryKeys(data_frame.to_dict())
      
      sql_statement = f'UPDATE {table_name} SET exported = 1, exportdatetime = "{dt.now()}", exportuserid = "{gs.spUserName}" WHERE id IN ({pk_list});'
      #print(sql_statement)
      db.executeSqlStatement(sql_statement)
              
      return 'Exported file to %s'%file_name
    else:
      return 'The table "%s" cannot be exported '%table_name

  def generateFilename(self, object_name, file_type, file_path):
    """
    Generic method for generating random filename including path denoting object type and timestamp 
    CONTRACT 
       object_name (String): Name of the object i.e. table to be generated file name for 
       file_type (String): Extension of the file type to be exported to 
       file_path (String): Path to the folder to be exported to 
       RETURNS Text string denoting the path and filename as specified. 
    """
    return tf.NamedTemporaryFile(prefix='%s-export_%s'%(object_name,dt.now().strftime("%Y%m%d%H%M_")), suffix='.%s'%file_type, dir=file_path).name

  def getPrimaryKeys(self, dict):
    """
    Method for extracting primary keys from dict into concatened string separated by commas 
    CONTRACT 
        dict (Dictionary): The dictionary containing the record rows 
    NOTE Must contain an 'id' field where the primary keys reside 
    """
    pk_list = ''
    pk_col = dict['id']
    for row in pk_col:
      pk_list = pk_list + str(pk_col[row]) + ', '
    pk_list = pk_list[0:len(pk_list)-2]
    
    return pk_list
