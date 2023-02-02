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
# from hashlib import new
import os
import sys
from pathlib import Path
import time
import logging
# from re import L
import util


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
    sTime = time.strftime('{%Y-%m-%d_%H,%M,%S}').replace("{", "").replace("}", "")

    filePath = tryout_Path()
    sys.path.append(str(Path(__file__).parent.parent.joinpath(filePath)))
    logName = f"{moduleName}-{sTime}.log"
    logFilePath = str(Path(filePath).joinpath(f'{logName}'))
    # print(logFilePath)
    logging.basicConfig(filename=logFilePath, encoding='utf-8', level=logging.DEBUG)

def tryout_Path():
    # Intended to return the True path in case OneDrive is running
    usrPath = util.getUserPath()
    altUsrPath = os.path.expanduser(
        '~\OneDrive - University of Copenhagen\Documents\DaSSCO')
    if os.path.isdir(usrPath):
        return usrPath
    elif os.path.isdir(altUsrPath):
        return altUsrPath
    else:
        error_message = f"Neither {usrPath} or {altUsrPath} exist."
        logging.debug(error_message)

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
#    Obtain application version number
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

