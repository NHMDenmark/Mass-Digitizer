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
from fileinput import filename
from tarfile import LENGTH_NAME
import pandas as pd
import tempfile as tf
from datetime import datetime as dt

# internal dependencies
import data_access as db

exportableTables = {'specimen'}

filePath = os.path.expanduser('~\Documents\DaSSCO') # In order to debug / run, a copy of the db file should be moved into this folder on Windows machines 
altFilePath = os.path.expanduser('~\OneDrive - University of Copenhagen\Documents\DaSSCO\db.sqlite3') # For OneDrive users this is the file location 

def exportSpecimens(file_type):
  # TODO method contract
  return exportTable('specimen', file_type)

def exportTable(table_name, file_type):
  # TODO method contract
  if table_name in exportableTables:
    db_df = pd.read_sql_query("SELECT * FROM %s WHERE exported IS NULL"%table_name, db.getConnection())
    try:
      file_name = generateFilename(table_name,file_type, filePath)
    except:
      file_name = generateFilename(table_name,file_type, altFilePath)
    db_df.to_excel(file_name)
    return 'Exported file to %s'%file_name
  else:
    return 'The table "%s" cannot be exported '%table_name

def generateFilename(object_name, file_type, file_path):
  # TODO method contract
  return tf.NamedTemporaryFile(prefix='%s-export_%s'%(object_name,dt.now().strftime("%Y%m%d%H%M_")), suffix='.%s'%file_type, dir=file_path).name

#exportTable('specimen','xlsx')
