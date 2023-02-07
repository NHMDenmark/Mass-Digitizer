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
   """
   Sets up logging for code module calling this method. 
   """
   # Generic logger: If imported and called it will allow - logging.debug(_your-message_). Log file is "moduleName&timeStamp"
   sTime = time.strftime('{%Y-%m-%d_%H,%M,%S}').replace("{", "").replace("}", "")

   #sys.path.append(str(Path(__file__).parent.parent.joinpath(getLogsPath)))
   logName = f"{moduleName}-{sTime}.log"
   logFilePath = str(Path(getLogsPath()).joinpath(logName))
   print(logFilePath)
   logging.basicConfig(filename=logFilePath, encoding='utf-8', level=logging.DEBUG)

""" def tryout_Path():
    db_lowerLimit = 1000 #DB size minimum limit for successful testing.
    # Intended to return the True path in case OneDrive is running. DB size testing will determine which path is returned.
    alternativePath = os.path.expanduser(r'~\OneDrive - University of Copenhagen\Documents\DaSSCO')
    regularPath = getUserPath()
    print('regular:', getUserPath(), type(getUserPath()))
    print('alternative:', alternativePath)
    test_regularDBPath = regularPath+'\db.sqlite3'
    print('regular DB:', test_regularDBPath)
    # usrPath = os.path.expanduser(getUserPath())
    # print("usrPath;;", type(usrPath), usrPath)
    test_altDBPath = os.path.expanduser(
        r'~\OneDrive - University of Copenhagen\Documents\DaSSCO\db.sqlite3') #Test on whether the DB is in the alternative user path
    sizeUserDB = None
    try:
        sizeUserDB = os.stat(test_regularDBPath)
    except Exception as e:
        logging.debug(e)

        pass
    sizeAlternativeDB = os.stat(test_altDBPath)


    sizeTest_altuserPath = os.stat(test_altDBPath)
    alternative_path_for_log = f'Alternative {sizeAlternativeDB} raw size : {sizeTest_altuserPath.st_size}'
    logging.debug(alternative_path_for_log)
    # Below is the size test on the regular path, and on the
    if sizeUserDB:
        if sizeUserDB.st_size > db_lowerLimit:
            print('regular :: ',sizeUserDB.st_size )
            return regularPath
    elif sizeTest_altuserPath.st_size > db_lowerLimit:
        print('alternative :: ', sizeAlternativeDB.st_size)
        return alternativePath
 """

def getLogsPath():
   return str(Path(getUserPath()).joinpath('logs'))

def getUserPath():
   """
   Get user documents path agnostic of OS or presence of OneDrive setup 
   """
   # Assuming regular system; Get regular user home path 
   homePath = str(Path(os.path.expanduser('~')))

   # Now check for existance of OneDrive user documents path 
   if "oneDrive" in os.environ:
      # OneDrive system if full user documents path exists,
      #  because that is where installer creates it:        
         oneDrivePath = os.environ['OneDrive']
         # If the full path exists then use the onedrivepath as home path 
         if os.path.exists(str(Path(oneDrivePath).joinpath('Documents').joinpath('DaSSCo'))):
            homePath = oneDrivePath   
   # Extend the user home path with  
   userPath = str(Path(homePath).joinpath('Documents').joinpath('DaSSCo'))
   
   return userPath

def logLine(line, level='info'):
   """
   Write a line to the log using the logging module initialized.  
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

def shrink_dict(original_dict, input_string):
   """
   Filter entries in dictionary based on initial string (starts with)
   """   
   shrunken_dict = {}
   
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

