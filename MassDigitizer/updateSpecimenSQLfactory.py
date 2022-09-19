# UPDATE employees
# SET lastname = 'Smith'
# WHERE employeeid = 3;
import json

def outer(tableName, recordID , fieldDict, update=False):

    if not update:
        print('NOT!!! UPDATING  //// but inserting')
    else:
        print('UPDATING')
        def assembleSQLupdate(tableName, recordID , fieldDict):
            # RecordID is the ID of record to be updated.
            # Dict are the field, value pairs for the update

            sql = f"UPDATE {tableName} SET "
            setList = []
            for key in fieldDict:
                print(key, fieldDict[key])
                setList.append(f"{key} = {fieldDict[key]}")
            sqlString = ', '.join(setList)

            print('SQL string = ', sqlString)
            sql = sql + sqlString + f" WHERE id = {recordID};"
            return sql
        assembleSQLupdate(tableName, recordID, fieldDict)

fields = {'catalognumber' : '22222222',
                      'multispecimen' : 'chkMultiSpecimen',
                      'taxonname'     : 'Grapsus',
                      'taxonnameid'   : '?',
                      'georegionname' : 'Nearctic',
                      'georegionid'   : 'georegion',
                      'storagename'   : '"%s"''cbxStorage',
                      'storageid'     : 'storage',
                      'preptypename'  : 'sheet',
                      'preptypeid'    : 'preptype',
                      'notes'         : 'just test',
                      'username'      : 'JKL',
                      #'userid'        : : '"%s"''txtUserName','username',
                      'workstation'   : 'PC'
                     }
res = outer('specimen' ,88, fields, update=True)
# res = assembleSQLupdate('specimen', 80, fields)
print(type(res), res)

#
# a = ['Tests run: one', ' Failures: 0', ' Errors: 0']
# b = dict([i.split(': ') for i in a])
# print('b - ', b, type(b))
# final = dict((k, int(v)) for k, v in fields.items())  # or iteritems instead of items in Python 2
# print(final, type(final))