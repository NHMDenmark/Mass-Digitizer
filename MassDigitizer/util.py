# -*- coding: utf-8 -*-
"""
  Created on June 24, 2022
  @author: Fedor Alexander Steeman, NHMD / Jan K. Legind, NHMD
  Copyright 2022 Natural History Museum of Denmark (NHMD)
  Licensed under the Apache License, Version 2.0 (the "License");
  you may not use this file except in compliance with the License.
  You may obtain a copy of the License at::
  http://www.apache.org/licenses/LICENSE-2.0
  Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for the specific language governing permissions and limitations under the License.

  PURPOSE: Assemblage of generic utility functions used across the application. 
"""

from os import system, name
# from hashlib import new
import os
import sys
from pathlib import Path
import time
import logging
# from re import L
import ctypes


def clear():
   """
   Clear Command Line Interface screen 
   """
   # for windows
   if name == 'nt':
      _ = system('cls')

   # for mac and linux
   else:
    _ = system('clear')

def buildLogger(moduleName):
    # Generic logger: If imported and called it will allow - logging.debug(_your-message_). Log file is "moduleName&timeStamp"
    sTime = time.strftime('{%Y-%m-%d_%H,%M,%S}').replace("{", "").replace("}", "")

    filePath = tryout_Path()
    sys.path.append(str(Path(__file__).parent.parent.joinpath(filePath)))
    logName = f"{moduleName}-{sTime}.log"
    logFilePath = str(Path(filePath).joinpath(logName))

    logging.basicConfig(filename=logFilePath, encoding='utf-8', level=logging.DEBUG)

def tryout_Path():
    db_lowerLimit = 1000
    # Intended to return the True path in case OneDrive is running. DB size testing will determine which path is returned.
    alternativePath = os.path.expanduser(r'~\OneDrive - University of Copenhagen\Documents\DaSSCO')
    regularPath = getUserPath()

    test_regularDBPath = f"{regularPath}\db.sqlite3"  #Test on whether the DB is in the regular user path
    usrPath = os.path.expanduser(getUserPath())
    # print("usrPath;;", type(usrPath), usrPath)
    test_altDBPath = os.path.expanduser(
        r'~\OneDrive - University of Copenhagen\Documents\DaSSCO\db.sqlite3') #Test on whether the DB is in the alternative user path

    sizeUserDB = os.stat(test_regularDBPath)
    sizeAlternativeDB = os.stat(test_altDBPath)
    regular_path_for_log = f'Regular {test_regularDBPath} raw size stat: {sizeUserDB.st_size}'
    logging.debug(regular_path_for_log)
    sizeTest_altuserPath = os.stat(test_altDBPath)
    alternative_path_for_log = f'Alternative {sizeAlternativeDB} raw size : {sizeTest_altuserPath.st_size}'
    logging.debug(alternative_path_for_log)
    # Below is the size test on the regular path, and on the
    if sizeUserDB.st_size > db_lowerLimit:
        return usrPath
    elif sizeTest_altuserPath.st_size > db_lowerLimit:
        return alternativePath
def shrink_dict(original_dict, input_string):
   """
   Filter entries in dictionary based on initial string (starts with)
   """   
   shrunken_dict = {}
   # print('Dictionary length = ', len(original_dict))
   for j in original_dict:
      if j[0:len(input_string)] == input_string:
         shrunken_dict[j] = original_dict[j]
   return shrunken_dict

def convert_dbrow_list(list, addEmptyRow=False):
   """
   Converts datarow list to name array 
   """
   new_list = []
   if addEmptyRow: new_list.append('-please select-')
   for item in list:
      new_list.append(item['name'])

   return new_list

# def pretty_pront_POST(req):
"""
Format HTTP request header and body into easily legible output.
Use pprint instead: 
import pprint 
pp = pprint.PrettyPrinter(indent=4)
pp.pprint(a_dict) || for JSON use json.dumps()
"""
# print('{}\n{}\r\n{}\r\n\r\n{}'.format(
#     '-----------START-----------',
#     req.method + ' ' + req.url,
#     '\r\n'.join('{}: {}'.format(k, v) for k, v in req.headers.items()),
#     req.body,
# ))
# print('------------END------------')

def getLogsPath():
   return str(Path(getUserPath()).joinpath('logs'))

def getUserPath():
    logsFilePath = os.path.expanduser(f'~\Documents\DaSSCO')
    return logsFilePath

def logLine(line, level='info'):
   """
   Log line 
   """
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

# def obtainVersionNumber(filepath, keyWord):
#    """
#    Obtain application version number from iss Inno setup file.
#    """
#
#    with open(filepath, mode='r') as f:
#         text = f.readlines()
#         version = ''
#         for line in text:
#             # check if string present on a current line
#             keyWord = '#define MyAppVersion'
#             # print(row.find(word))
#             # find() method returns -1 if the value is not found,
#             # if found it returns index of the first occurrence of the substring
#             if line.find(keyWord) != -1:
#                 versionSplit = line.split(' ')
#                 versionPop = versionSplit.pop()
#                 # print(versionPop.replace('"', ''))
#                 return versionPop.replace('"', '')

class Struct:
    """A structure that can have any fields defined."""
    def __init__(self, **entries): self.__dict__.update(entries)

