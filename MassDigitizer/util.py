# -*- coding: utf-8 -*-
"""
  Created on June 24, 2022
  @author: Fedor Alexander Steeman, NHMD
  Copyright 2022 Natural History Museum of Denmark (NHMD)
  Licensed under the Apache License, Version 2.0 (the "License");
  you may not use this file except in compliance with the License.
  You may obtain a copy of the License at
  http://www.apache.org/licenses/LICENSE-2.0
  Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for the specific language governing permissions and limitations under the License.

  PURPOSE: Assemblage of generic utility functions used across the application. 
"""

from os import system, name
from hashlib import new
import logging
from re import L

# Internal dependencies
import data_access
import global_settings as gs

db = data_access.DataAccess(gs.databaseName)

def clear():
   # Clear CLI screen 
   # for windows
   if name == 'nt':
      _ = system('cls')

   # for mac and linux
   else:
    _ = system('clear')

def shrink_dict(original_dict, input_string):
   # TODO Complete function contract
   # Filter entries in dictionary based on initial string (starts with)

   shrunken_dict = {}
   print('Dictionary length = ', len(original_dict))
   for j in original_dict:
      if j[0:len(input_string)] == input_string:
         shrunken_dict[j] = original_dict[j]
   return shrunken_dict

def convert_dbrow_list(list, addEmptyRow=False):
   # TODO complete function contract
   # Converts datarow list to name array 
   new_list = []
   if addEmptyRow: new_list.append('-please select-')
   for item in list:
      new_list.append(item['name'])

   return new_list

def pretty_print_POST(req):
   # TODO description  
    """
    At this point it is completely built and ready
    to be fired; it is "prepared".

    However pay attention at the formatting used in 
    this function because it is programmed to be pretty 
    printed and may differ from the actual request.
    """
    print('{}\n{}\r\n{}\r\n\r\n{}'.format(
        '-----------START-----------',
        req.method + ' ' + req.url,
        '\r\n'.join('{}: {}'.format(k, v) for k, v in req.headers.items()),
        req.body,
    ))
    print('------------END------------')

def getPrimaryKey(tableName, name, field='name'): 
   # Function for fetching id (primary key) on name value
   return db.getRowsOnFilters(tableName, {' %s = ' % field: '"%s"' % name})[0]['id']

def logLine(line, level='info'):
   
   logging.basicConfig(filename='example.log', encoding='utf-8', level=logging.DEBUG)

   if(level == 'info'):
      logging.info(line)
   elif(level == 'debug'):
      logging.debug(line)
   elif(level == 'warning'):
      logging.warning(line)
   elif(level == 'error'):
      logging.error(line)
   else:
      logging.info(line)

   return line

def obtainVersionNumber(filepath, keyWord):
    with open(filepath, mode='r') as f:
        text = f.readlines()
        version = ''
        for line in text:
            # check if string present on a current line
            keyWord = '#define MyAppVersion'
            # print(row.find(word))
            # find() method returns -1 if the value is not found,
            # if found it returns index of the first occurrence of the substring
            if line.find(keyWord) != -1:

                versionSplit = line.split(' ')
                print(versionSplit)
                versionPop = versionSplit.pop()
                print(versionPop.replace('"', ''))
                return versionPop.replace('"', '')

class Struct:
    "A structure that can have any fields defined."
    def __init__(self, **entries): self.__dict__.update(entries)