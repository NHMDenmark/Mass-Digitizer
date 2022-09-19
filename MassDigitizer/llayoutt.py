import PySimpleGUI as sg
import os
import sys
import pathlib

# internal dependencies
import util
import data_access as db
import global_settings as gs
# import home_screen as hs
import kick_off_sql_searches as koss

# Make sure that current folder is registrered to be able to access other app files
sys.path.append(str(pathlib.Path(__file__).parent.parent.joinpath('MassDigitizer')))
currentpath = os.path.join(pathlib.Path(__file__).parent, '')

collectionId = -1


# Function for converting predefined table data into list for dropdownlist
def getList(tablename, collectionid): return util.convert_dbrow_list(
    db.getRowsOnFilters(tablename, {'collectionid =': '%s' % collectionid}))


# Function for fetching id (primary key) on name value
def getPrimaryKey(tableName, name, field='name'): return \
db.getRowsOnFilters(tableName, {' %s = ' % field: '"%s"' % name})[0]['id']  # return db.getRowsOnFilters(tableName, {' %s = ':'"%s"'%(field, name)})[0]['id']