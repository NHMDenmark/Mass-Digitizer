# -*- coding: utf-8 -*-
"""
Created on Thu May 26 17:44:00 2022
@authors: Jan K. Legind, NHMD;
Copyright 2022 Natural History Museum of Denmark (NHMD)
Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at
http://www.apache.org/licenses/LICENSE-2.0
Unless required by applicable law or agreed to in writing,
software distributed under the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND,
either express or implied. See the License for the specific language governing permissions and limitations under the License.
- CAN ONLY BE USED TO MONITOR A Windows Machine!!!
- The code adds three new required columns to Digi app files coming into the monitored directory.
"""
import os
import win32file
import win32event
import win32con

import pandas as pd
import csv # for the delimiter sniffer
import cchardet as chardet # for file encoding sniffer
import sys

path_to_watch = os.path.abspath (r"N:\SCI-SNM-DigitalCollections\DaSSCo\DigiApp\Data\2.PostProcessed_openRefine\a_test_monitor") # 'a_test_monitor' should be removed to make the path operational.
print(path_to_watch)

''' FindFirstChangeNotification sets up a handle for watching
  file changes. The first parameter is the path to be
  watched; the second is a boolean indicating whether the
  directories underneath the one specified are to be watched;
  the third is a list of flags as to what kind of changes to
  watch for. We're just looking at file additions / deletions.'''

change_handle = win32file.FindFirstChangeNotification (
  path_to_watch,
  0,
  win32con.FILE_NOTIFY_CHANGE_FILE_NAME
) # change_handle is a global used later for determining the type of change occurring in a directory.

def fileNameGetDate(filename):
    #A very specific function for extracting the date string as ISO date (yyyy-MM-dd) from the file name itself. Example: NHMD_Herba_20230913_15_55_RL.csv
    tokens = None
    if '-' in filename:
        tokens = filename.split('-')
    else:
        tokens = filename.split('_')
    print(f"TOKENS!!!!!! for {filename}", tokens)
    fileDate = f"{tokens[2]}"
    year = fileDate[0:4]
    month = fileDate[4:6]
    day = fileDate[6:8]
    isoDate = f"{year}-{month}-{day}"
    return isoDate

def getDelimiter(filePath):
    '''
    The file delimiter might not always be the same so a delimiter sniffer is useful.
    :param filePath: Must be the absolute path
    :return: the *sv delimiter
    '''
    with open(filePath, 'r') as f1:
        dialect = csv.Sniffer().sniff(f1.read()) #### detect delimiters
        f1.seek(0)
        print(f"dialect.delimiter --{dialect.delimiter}--")

        match dialect.delimiter:
            case '\t':
                print("Delimiter is TAB")
                return "\t"
            case ';':
                return ";"
            case ',':
                return ','
            case '|':
                return '|'
            case _: #This is the default case
                return dialect.delimiter
                print("Error, no recognized delimiter found!")

def encodingSniffer(fileName):
    '''
     Made to check the file encoding. Will mainly be utf-8 or windows-1252 (ANSI)
    :param fileName: Absolute file path
    :return: the encoding as a string
    '''
    with open(f"{fileName}", "rb") as f:
        msg = f.read()
        result = chardet.detect(msg)
        print('THE .result.:', result)
        enc = result['encoding']
        match enc:
            case 'ASCII':
                return 'Windows-1252'
            case 'UTF-8':
                return 'UTF-8'
            case 'UTF-8-SIG':
                return 'UTF-8'
            case _:
                print('unknown encoding')
                return 'Windows-1252'

def addColumnsToDf(myDf, filename):
    ''' Adds three specific columns see https://github.com/NHMDenmark/Mass-Digitizer/issues/461#issuecomment-1953535744
    myDf is generated in the exe part of the code and comes from the file added to the monitored directory
    :returns the df with the three added columns
    '''
    header = myDf.columns.to_list()
    print(myDf.head(2).to_string())
    dateString = fileNameGetDate(filename)

    # Columns added to satisfy the tabular remarks requirements
    myDf['datafile_date'] = dateString
    myDf['datafile_remark'] = filename
    myDf['datafile_source'] = 'DaSSCo data file'

    return myDf

def dfToFile(myDf, filename, name_extension=''):  # name_extension can be 'original'...
    # Write the *SV processed file in place of the original. This file will be ready to transfer into the 'PostProcessed' directory
    outputPath = f"{path_to_watch}/{filename}"
    print('&&&&&&&', outputPath)
    if name_extension:
        tokenPath = outputPath.split('.')
        print(tokenPath)
    delimiter = getDelimiter(outputPath)
    coda = encodingSniffer(outputPath)

    df.to_csv(outputPath, sep=delimiter, index=False, header=True, encoding=coda)
    return "TSV saved :)"

#
# Loop forever, listing any file changes. The WaitFor... will
#  time out every half a second allowing for keyboard interrupts
#  to terminate the loop.
#
try:

  old_path_contents = dict ([(f, None) for f in os.listdir (path_to_watch)])
  while 1:
    result = win32event.WaitForSingleObject (change_handle, 500)

    #
    # If the WaitFor... returned because of a notification (as
    #  opposed to timing out or some error) then look for the
    #  changes in the directory contents.
    #
    if result == win32con.WAIT_OBJECT_0:
      new_path_contents = dict ([(f, None) for f in os.listdir (path_to_watch)])
      added = [f for f in new_path_contents if not f in old_path_contents] # compare old to new content
      deleted = [f for f in old_path_contents if not f in new_path_contents] # the inverse of above
      if added:
          try:
            filename = ", ".join(added)
            filePath = f"{path_to_watch}/{filename}"
            delimiter = getDelimiter(f"{path_to_watch}/{filename}")
            fileEncoding = encodingSniffer(filePath)
            df = pd.read_csv(filePath, sep=delimiter, encoding=fileEncoding, converters={'agentlastname':lambda x:x.replace('/r','')}) # the converter is there to prevent pandas read_csv() from including new lines in the lastname  
            # WARNING, currently Specify workbench expects cp-1252 encoded files. Might change in the future!
            df = addColumnsToDf(df, filename)
            res = dfToFile(df, filename, name_extension='_original')
            print(res)
          except PermissionError as e: # A silly error that does not affect the desired result, i.e. the end output file. I was not able to get to the root of this error
             continue

      if deleted: print("Deleted: ", ", ".join (deleted))

      old_path_contents = new_path_contents
      win32file.FindNextChangeNotification (change_handle)

finally:
  win32file.FindCloseChangeNotification (change_handle)
