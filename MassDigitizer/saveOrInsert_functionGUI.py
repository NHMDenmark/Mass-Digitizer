# -*- coding: utf-8 -*-
"""
Created on Thu May 26 17:44:00 2022

@authors: Jan K. Legind, NHMD; Fedor A. Steeman NHMD

Copyright 2022 Natural History Museum of Denmark (NHMD)

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing,
software distributed under the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND,
either express or implied. See the License for the specific language governing permissions and limitations under the License.
"""

from datetime import datetime
import pytz
import data_access as db


def saving_to_db(fields, insert=True, recordID=None):
    # fields must be a dictionary with the specimen table headers as 'keys' and the form field content as 'values'.
    # insert is a switch to mark whether an INSERT or an UPDATE is called for.
    # recordID is required for updates.

    if insert:
        # Checking if Save is a novel record , or if it is updating existing record.
        print('We are inserting! ')
        print('Saving now ', datetime.now(pytz.timezone("Europe/Copenhagen")))
        sql_res = db.insertRow('specimen', fields)

        return sql_res
    else:
        print('We are updating! ')
        print('the row with ID - ', recordID)
        update = db.updateRow('specimen', recordID, fields)
        print(update)
