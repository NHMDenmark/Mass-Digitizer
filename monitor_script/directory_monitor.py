import os

import win32file
import win32event
import win32con

import pandas as pd

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
)


def addColumnsToDataFrame(myDf, filename):
    # Adds three specific columns see https://github.com/NHMDenmark/Mass-Digitizer/issues/461#issuecomment-1953535744
    dateString = fileNameGetDate(filename) # Obtains the ISO date from the filename.
    df['datafile_date'] = dateString
    df['datafile_remark'] = filename
    df['datafile_source'] = 'DaSSCo data file'

def fileNameGetDate(filename):
    #A very specific function for extracting the date string as ISO date (yyyy-MM-dd) from the file name itself.
    tokens = filename.split('-')
    fileDate = f"{tokens[2]}"
    year = fileDate[0:4]
    month = fileDate[4:6]
    day = fileDate[6:8]
    isoDate = f"{year}-{month}-{day}"
    return isoDate

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
      added = [f for f in new_path_contents if not f in old_path_contents]
      deleted = [f for f in old_path_contents if not f in new_path_contents]
      if added:
        print("Added: ", ", ".join (added))
        filename = ", ".join (added)
        try:
            df = pd.read_csv(f"{path_to_watch}/{filename}", sep='\t')
        except PermissionError:
            continue

        print(list(df.columns))
        dateString = fileNameGetDate(filename)
        df['datafile_date'] = dateString
        df['datafile_remark'] = filename
        df['datafile_source'] = 'DaSSCo data file'
        print(df.head(5).to_string())
        outputPath = f"{path_to_watch}/{filename}"
        df.to_csv(outputPath, sep='\t', index=False, header=True)
          
      if deleted: print("Deleted: ", ", ".join (deleted))

      old_path_contents = new_path_contents
      win32file.FindNextChangeNotification (change_handle)

finally:
  win32file.FindCloseChangeNotification (change_handle)