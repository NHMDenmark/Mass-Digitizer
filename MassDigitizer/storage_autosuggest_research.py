
import data_access as db
import fnmatch
from timeit import default_timer as timer
from datetime import timedelta


start = timer() #performance measure start
sql = "SELECT name, fullname FROM storage"
rows = db.executeSqlStatement(sql)
storageDict = {}
for j in rows:
    storageDict[j['name']] = j['fullname']

end = timer() #end of measuring the timedelta of populating the storageDict.
print('Time performance for populating dictionary storageDict= ', timedelta(seconds=end-start))

print(len(storageDict))

def storage_autosuggest(partialName, storage_dictionary):

    print('IN storage_auto!! partial=', partialName)
    keys = fnmatch.filter(storage_dictionary, "Box 38*")
    # fnmatch is a unix style pattern matching module
    print('length return dict: ', len(keys))

    return keys

suggestions = storage_autosuggest('Box 38', storageDict)
print(suggestions)
end = timer()
print('performance running the entire module= ', timedelta(seconds=end-start))