from datetime import datetime
import pytz
import data_access as db


def saving(fields, insert=True):
    if insert:

        # Checking if Save is a novel record , or if it is updating existing record.
        print('We are inserting! ')
        # currentID = existingRecordID
        # db.getRowsOnFilters('specimen', {'id': '= ' + str(recordID_forSave)}, limit=1)
        print('Saving now ', datetime.now(pytz.timezone("Europe/Copenhagen")))
        sql = db.insertRow('specimen', fields)
        print('insert SQL is :::', sql)
