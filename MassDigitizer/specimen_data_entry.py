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

import os
import sys
import pathlib
from datetime import datetime
import PySimpleGUI as sg
import pytz
# internal dependencies
import util 
import data_access as db
import global_settings as gs
import home_screen as hs 
import kick_off_sql_searches as koss

# Make sure that current folder is registrered to be able to access other app files 
sys.path.append(str(pathlib.Path(__file__).parent.parent.joinpath('MassDigitizer')))
currentpath = os.path.join(pathlib.Path(__file__).parent, '')

collectionId = -1
selectionIndex = 0
global indexer
indexer = []
def getIncrementedIndex(currentIndex):
    global indexer
    print('indexer now: ', indexer)
    if currentIndex == -1:
        indexer.pop()
    indexer.append(currentIndex)
    countElements = len(indexer)
    return countElements

# Function for converting predefined table data into list for dropdownlist 
def getList(tablename, collectionid): return util.convert_dbrow_list(db.getRowsOnFilters(tablename,{'collectionid =':'%s'%collectionid}))

# Function for fetching id (primary key) on name value 
def getPrimaryKey(tableName, name, field='name'):
    return db.getRowsOnFilters(tableName, {' %s = '%field : '"%s"'%name})[0]['id'] # return db.getRowsOnFilters(tableName, {' %s = ':'"%s"'%(field, name)})[0]['id']

def init(collection_id):
    # TODO function contract 

    # Set collection id  
    collectionId = collection_id
    c = collection_id

    # Define UI areas
    sg.theme('SystemDefault')
    greenArea = '#E8F4EA'   # Stable fields 
    blueArea = '#99ccff'    # Variable fields 
    greyArea = '#BFD1DF'    # Session & Settings 

    defaultSize = (21,1)    # Ensure element labels are the same size so that they line up
    element_size = (30,1)   # Default width of all fields in the 'green area' 
    blue_size = (28,1)      # Default width of all fields in the 'blue area'
    
    font = ('Bahnschrift', 13)
    
    # TODO placeholder until higher taxonomic groups become available in SQLite 
    taxonomicGroups = ['placeholder...']

    # Store elements in variables to make it easier to include and position in the frames
    storage = [sg.Text("Storage location:", size=defaultSize, background_color=greenArea, font=font),
               sg.Combo(getList('storage',c), key='cbxStorage', size=element_size, text_color='black', background_color='white', font=('Arial', 12), readonly=True, enable_events=True),]
    preparation = [sg.Text("Preparation type:", size=defaultSize, background_color=greenArea, font=font),
                   sg.Combo(getList('preptype',c), key='cbxPrepType', size=element_size, text_color='black', background_color='white',font=('Arial', 12), readonly=True, enable_events=True),]
    taxonomy = [sg.Text("Taxonomic group:", size=defaultSize, visible=False, background_color=greenArea, font=font),
                sg.Combo(taxonomicGroups, key='cbxHigherTaxon', visible=False, size=element_size, text_color='black', background_color='white', font=('Arial', 12), readonly=True, enable_events=True),]
    type_status = [sg.Text('Type status:', size=defaultSize, background_color=greenArea, font=font),
                   sg.Combo(getList('typeStatus',c), key='cbxTypeStatus', size=element_size, text_color='black', background_color='white', font=('Arial', 12), readonly=True, enable_events=True),]
    notes = [sg.Text('Notes', size=defaultSize, background_color=greenArea, font=font),
             sg.Multiline(size=(31,5), background_color='white', text_color='black', key='txtNotes', enable_events=False)]
    layout_greenarea = [storage, preparation, taxonomy, type_status, notes, 
                        [sg.Checkbox('Multispecimen sheet', key='chkMultiSpecimen', background_color=greenArea, font=(11))],]
    broadGeo = [sg.Text('Broad geographic region:', size=defaultSize ,background_color=blueArea, text_color='black', font=font),
                sg.Combo(getList('georegion',c), size=blue_size, key='cbxGeoRegion', text_color='black', background_color='white', font=('Arial', 12), readonly=True, enable_events=True),]
    taxonInput = [sg.Text('Taxonomic name:     ', size=(21,1) ,background_color=blueArea, text_color='black', font=font),
                  sg.Input('', size=blue_size, key='txtTaxonName', text_color='black', background_color='white', font=('Arial', 12), enable_events=True, pad=((5,0),(0,0))),]
    taxonomicPicklist = [sg.Text('', size=defaultSize, background_color=blueArea, text_color='black', font=font),
                         sg.Listbox('', key='cbxTaxonName', select_mode='browse', size=(28, 6), text_color='black', background_color='white', font=('Arial', 12),bind_return_key=True, enable_events=True, pad=((5, 0), (0, 0))), ]
    barcode = [sg.Text('Barcode:', size=defaultSize, background_color=blueArea, enable_events=True, text_color='black', font=font),
               sg.InputText('', key='txtCatalogNumber', size=blue_size, text_color='black', background_color='white', font=('Arial', 12), enable_events=True),]
    # statusLabel = [sg.Text('Specimen record has been saved', font=('Arial',20),size=(20,10),justification='center',background_color='#4f280a',text_color = 'yellow',key='texto')]


    layout_bluearea = [broadGeo, taxonInput, taxonomicPicklist, barcode,

        [sg.Text('Record ID: ', key='lblRecordID', background_color='#99dcff', visible=True, size=(12,1)),
         sg.StatusBar('', relief=None, size=(10,1), background_color=blueArea),
         sg.Button('SAVE', key="btnSave", button_color='seagreen', size=9, bind_return_key=True),
         sg.StatusBar('', relief=None, size=(14,1), background_color=blueArea),
         sg.Button('Go Back', key="btnBack", button_color='firebrick', pad=(130,0))]]
    loggedIn = [sg.Text('Logged in as:', size=defaultSize, background_color=greyArea, font=font), sg.Input(disabled=True, size=(24,1), background_color='white', text_color='black',
                readonly=True, key='txtUserName'),]
    institution_ = [sg.Text('Institution:', size=defaultSize, background_color=greyArea, font=font), sg.Input(size=(24,1), background_color='white', text_color='black', 
                readonly=True, key="txtInstitution"),]
    collections =  [sg.Text('Collection:', size=defaultSize, background_color=greyArea, font=font), sg.Input(size=(24,1), background_color='white', text_color='black', 
                readonly=True, key="txtCollection"),]
    work_station =  [sg.Text('Workstation:', size=defaultSize, background_color=greyArea, font=font), sg.Input(size=(24,1), background_color='white', text_color='black', 
                readonly=True, key="txtWorkStation"),]
    settings_ = [sg.Text('Settings ', size=defaultSize, justification='center', background_color=greyArea, font=14), 
                 sg.Button('', image_filename='%soptions_gear.png'%currentpath, key='btnSettings', button_color=greyArea, border_width=0)]
    horizontal_line = [sg.Text("_______________" * 5, background_color=greyArea)] # horizontal line element hack
    layout_greyarea = [loggedIn, institution_, horizontal_line, collections, work_station, settings_, [sg.Button('LOG OUT', key="btnLogout", button_color='grey40')]]

    # Combine elements into full layout
    layout = [[sg.Frame('',  [[sg.Column(layout_greenarea, background_color=greenArea)]], size=(250,200), expand_x=True, expand_y=True, background_color=greenArea),
               sg.Frame('', [[sg.Column(layout_greyarea, background_color=greyArea)]], size=(250, 300), expand_x=True, expand_y=True, background_color=greyArea)],
              [sg.Frame('',   [[sg.Column(layout_bluearea, background_color=blueArea)]], expand_x=True, expand_y=True, background_color=blueArea, title_location=sg.TITLE_LOCATION_TOP)],]

    window = sg.Window("Mass Annotated Digitization Desk  (MADD)", layout, margins=(2, 2), size=(950,580), resizable=True, return_keyboard_events=True, finalize=True )
    window.TKroot.focus_force()
    window['cbxTaxonName'].bind("<Return>", "_Enter")
    window['chkMultiSpecimen'].bind("<Return>", "_Enter")
    window.Element('txtUserName').Widget.config(takefocus=0)
    window.Element('txtInstitution').Widget.config(takefocus=0)
    window.Element('txtCollection').Widget.config(takefocus=0)
    window.Element('txtWorkStation').Widget.config(takefocus=0)
    window.Element('btnSettings').Widget.config(takefocus=0)
    window.Element('btnLogout').Widget.config(takefocus=0)


    entry_barcode = window['txtCatalogNumber']
    entry_barcode.bind("<Return>", "_RETURN")
    # Above forces a <RETURN> when barcode is scanned. This requires the scanner
    # to be set to <ENTER>. See scanner user manual.

    # The three lines below are there to ensure that the cursor in the input text fields is visible. It is invisible against a white background.
    #window['txtNotes'].Widget.config(insertbackground='black', highlightcolor='firebrick', highlightthickness=2)
    #window['txtUserName'].Widget.config(insertbackground='black', highlightcolor='firebrick', highlightthickness=2)
    #window['-TAXNAMES-'].Widget.config(insertbackground='black') , highlightcolor='firebrick', highlightthickness=2)

    # Set session Widget fields
    window.Element('txtUserName').Update(value=gs.spUserName) 
    collection = db.getRowOnId('collection', collection_id)
    print('collection isss: ', collection[2])
    if collection is not None:
        window.Element('txtCollection').Update(value=collection[2]) 
        institution = db.getRowOnId('institution', collection[3])
        window.Element('txtInstitution').Update(value=institution[2]) 
    window.Element('txtWorkStation').Update(value='TRS-80')
    window['txtNotes'].bind('<Tab>', '+TAB')
    window['cbxStorage'].set_focus()

    # Reset taxonname field 
    currrent_selection_index = 0
    window.Element('cbxTaxonName').Update(set_to_index=0)  # Start with first item highlighted

    # Loop through events
    # backtrackCounter = 0


    def getRecordIDbyBacktracking(backtrackCounter):
        sql = "select * from specimen s  order by s.id DESC LIMIT {},1;".format(backtrackCounter)
        rows = db.executeSqlStatement(sql)
        print('COUNTER row::::', rows[0])
        recordIDcurrent = rows[0]['id']
        return recordIDcurrent

    dasRecordID = 0
    # Yes , it is a global var :[
    def obtainTrack(ID=0, incrementor=0):
        # Keeps track of record IDs in relation to the Go-back button functionality.
        print('the obtain ID  is --', ID)
        if ID == 0:
            print('IN ID of obtainTrack()')
            recordID = getRecordIDbyBacktracking(incrementor)
            return recordID
        else:
            print('In ELSE obtainTrack()')
            recordID = ID - 1
            return recordID

    onecrementor = 0

    while True:
        event, values = window.read()

        # Checking field events as switch construct 
        if event == 'cbxStorage':
            print('event:', event)
            print('In storage domain')
        if event == 'cbxPrepType':
            print('In preparation type')
            prepper = values[event]

        if event == 'cbxHigherTaxon':
            print('IN taxonomy section')
        if event == 'cbxTypeStatus':
            print('IN type status section')
        if event == 'txtNotes':
            print('IN notes section')
        if event.endswith('+TAB'):
            window['chkMultiSpecimen'].set_focus()
        #     Prevents tab characters in the Notes box and allows to tab on to next element.
        # if event.endswith('+TAB'):
        #     window['cbxGeoRegion'].set_focus()
        if event == 'chkMultiSpecimen_Enter':
            print('Multi specimen herbarium sheet was set to TRUE')
            window['chkMultiSpecimen'].update(True)
            window['cbxGeoRegion'].set_focus()
        if event == 'txtTaxonName':
            input_ = values['txtTaxonName']
            print('in taxon input -')
            # print('len string : ', len(values[event]))
            if len(values[event]) >= 2:

                print('submitted string: ', values[event])
                response = koss.auto_suggest_taxonomy(values[event])
                if response is not None:
                    print('Suggested taxa based on input:) -- ', response)
                    window['cbxTaxonName'].update(values=response)
                    window['cbxTaxonName'].update(set_to_index=[0], scroll_to_index=0)
                    # selection_index = 0
                    # if event.startswith('Up'):
                    #     selectionIndex = (currentIndex - 1) % len(window['cbxTaxonName'])
                    #     print('UP and index is ', selectionIndex)
                    #     window['cbxTaxonName'].Update(set_to_index=selectionIndex, scroll_to_index=selectionIndex)
                    # if event.startswith('Down'):
                    #     selectionIndex = (currentIndex + 1) % len(window['cbxTaxonName'])
                    #     print('DOWN and index is ', selectionIndex)
                    #     window['cbxTaxonName'].Update(set_to_index=selectionIndex, scroll_to_index=selectionIndex)
        #             Forces 1st item in list to be highlighted which makes it selectable by Return key
        # down = False
        if event.startswith('Down'):
            print('In DOWN press')
            sizeAutosuggest = len(response)
            # print('length of cbx is : ', sizeAutosuggest)
            selectionIndex = getIncrementedIndex(1) % sizeAutosuggest
            print('selection index= ', selectionIndex)
            window['cbxTaxonName'].Update(set_to_index=selectionIndex, scroll_to_index=selectionIndex)
        if event.startswith('Down'):
            print('In UP press')
            sizeAutosuggest = len(response)
            # print('length of cbx is : ', sizeAutosuggest)
            selectionIndex = getIncrementedIndex(-1) % sizeAutosuggest
            print('selection index= ', selectionIndex)
            window['cbxTaxonName'].Update(set_to_index=selectionIndex, scroll_to_index=selectionIndex)

        if event == 'cbxTaxonName':
            if event.startswith('Down'):
                print('down is -v')
            # if down: print('DOWM')
            if event.startswith('Up'): print('UP')
            index = 0 # Reset highlighted item 
            window['cbxTaxonName'].update(scroll_to_index=index)
            if event.startswith('Up'):
                print('UP')
                # selectionIndex = (currentIndex - 1) % len(window['cbxTaxonName'])
                # print('UP and index is ', selectionIndex)
                # window['cbxTaxonName'].Update(set_to_index=selectionIndex, scroll_to_index=selectionIndex)
            if event.startswith('Down'):
                print('DOWN')
                # selectionIndex = getIncrementedIndex(1) % len(window['cbxTaxonName'])
                print('DOWN and index is ', selectionIndex)
                window['cbxTaxonName'].Update(set_to_index=selectionIndex, scroll_to_index=selectionIndex)
            selection = values[event]
            print('selection ;', selection)
            if selection:
                item = selection[0]
                print('item at selection=', item)

        elif event == "cbxTaxonName" + "_Enter": # For arrowing down to relevant taxon name and pressing Enter
            window['txtTaxonName'].update(values['cbxTaxonName'][0])
            print(f"InputTax: {values['cbxTaxonName'][0]}")

        if event == "txtCatalogNumber_RETURN":
            print('vals= ', values)
            print(f"Input barcode yowsa: {values['txtCatalogNumber']}")
            window['btnSave'].set_focus()

        if event == 'btnLogout':
            gs.clearSession()
            hs.window.reappear()
            window.close()

        # Save form
        unpackedTaxonName = ''
        if values:
            taxonName = values['cbxTaxonName']
            for item in taxonName: taxonName = item
            print('PREP back/save cbxTaxonName == ', unpackedTaxonName)

            if not taxonName:
                taxonName = values['txtTaxonName']
                # for item in taxonName: unpackedTaxonName = item
                print('txtTaxonName bist: : ', taxonName)

        if event == 'btnSave':
            # print('after save press /updating/ var...', is_update)
            fields = {'catalognumber': '"%s"' % values['txtCatalogNumber'],
                      'multispecimen': values['chkMultiSpecimen'],
                      'taxonname': '"%s"' % taxonName,
                      'taxonnameid': getPrimaryKey('taxonname', taxonName, 'fullname'),
                      'typestatusid': getPrimaryKey('typestatus', values['cbxTypeStatus']),
                      'georegionname': '"%s"' % values['cbxGeoRegion'],
                      'georegionid': getPrimaryKey('georegion', values['cbxGeoRegion']),
                      'storagename': '"%s"' % values['cbxStorage'],
                      'storageid': getPrimaryKey('storage', values['cbxStorage']),
                      'preptypename': '"%s"' % values['cbxPrepType'],
                      'preptypeid': getPrimaryKey('preptype', values['cbxPrepType']),
                      'notes': '"%s"' % values['txtNotes'],
                      'collectionid': collectionId,
                      'username': '"%s"' % values['txtUserName'],
                      # 'userid'        : getPrimaryKey('"%s"'%values['txtUserName'],'username'),
                      'workstation': '"%s"' % values['txtWorkStation'],
                      'datetime': '"%s"' % datetime.now(),
                      }
            # for k, v in fields.items():
            #     if isinstance(v, str):
            #         fields[k] = v.replace('"','')
            #     else:
            #         pass
            print('FIELDS ::: : ', fields)

            # recordID_forSave = getRecordIDbyBacktracking(0)
            recordID = dasRecordID
            print('pre existing id ...recordID == ', recordID)
            if recordID > 0:
                # Checking if Save is a novel record , or if it is updating existing record.
                print('We are updating! ')
                currentID = recordID
                    # db.getRowsOnFilters('specimen', {'id': '= ' + str(recordID_forSave)}, limit=1)

                print('the row with ID - ', currentID)
                topicalRecordID = currentID
                db.updateRow('specimen', topicalRecordID, fields)

            else:
                print('Saving now ', datetime.now(pytz.timezone("Europe/Copenhagen")))
                db.insertRow('specimen', fields)

            # def saveButtonBehavior(fieldDict, recordID):
            #     pass

            # def setSaveButton(tableName, fieldDict, updating=is_update):
            #     print('IN setsaveButton - status update === ', updating)
            #     opsSQL = ''
            #     if updating:
            #         print('is UPDATING')
            #
            #         def assembleSQLupdate(tableName, recordID , fields):
            #             # RecordID is the ID of record to be updated.
            #             # Dict are the field, value pairs for the update
            #             print('fields is ¤¤¤¤ - ', fields)
            #             sql = f"UPDATE {tableName} SET "
            #             setList = []
            #             for key in fields:
            #                 print(key, fieldDict[key])
            #                 setList.append(f"{key} = {fieldDict[key]}")
            #             sqlString = ', '.join(setList)
            #
            #             print('SQL string = ', sqlString)
            #             sql = sql + sqlString + f" WHERE id = {recordID};"
            #             return sql
            #
            #         recordID = getRecordIDbyBacktracking(backtrackCounter)
            #         returnedSQL = assembleSQLupdate(tableName, recordID, fieldDict)
            #         print('RETURNED SQL is :_: ', returnedSQL)
            #
            #         opsSQL = returnedSQL
            #         is_update = False
            #
            #         res = setSaveButton('specimen', fields)
            #         print('the /res/ is == ', res)
            #     else:
            #
            #         print('Saving form')
            #
            #         taxonName = ''
            #         if len(values['txtCatalogNumber']) > 0:
            #             print('in catalognumber')
            #             taxonName = values['txtTaxonName']
            #         window['txtCatalogNumber'].update([])
            #         print(fields)
            #         db.insertRow('specimen', fields)
            #         window['txtCatalogNumber'].set_focus()  # returns focus to barcode field after 'save'
            #
            #     return opsSQL

            # mintedID = setSaveButton('specimen', fields)


        if event == 'btnBack':
            print('Pressed go-back /')

            # Functionality for going back through the session records to make changes, or do checkups.
            currentRecordID = obtainTrack(incrementor=onecrementor)
            onecrementor += 1
            print('oneicrementor at -- ', onecrementor)
            print('current recordID :  ', currentRecordID)
            rows = db.getRowOnId('specimen', currentRecordID)
            print('RAW row::::', rows[0])
            recordIDbacktrack = rows[0]
            dasRecordID = recordIDbacktrack
            print('record past ID : ', recordIDbacktrack)
            rowRecord = db.getRowOnId('specimen', currentRecordID)
            record = rowRecord

            if recordIDbacktrack:
                print('recordbactrack - // is_update IS TRUE')
                is_update = True

            else :
                is_update = False

            print('the backtrack counter is now at: ', recordIDbacktrack)
            print('the ID of interest is= ', recordIDbacktrack)

            window['lblRecordID'].update('Record ID: {}'.format(recordIDbacktrack), visible=True)
            # Updating elements from previous record
            window['cbxStorage'].update(record['storagename'])
            window['cbxPrepType'].update(record['preptypename'])
            window['cbxHigherTaxon'].update('')
            window['cbxTypeStatus'].update('')
            window['txtNotes'].update(record['notes'])
            # multiSpecimen??
            window['cbxGeoRegion'].update(record['georegionname'])
            window['txtTaxonName'].update(record['taxonname'])
            window['cbxTaxonName'].update([])
            window['txtCatalogNumber'].update(record['catalognumber'])

            fields = {'catalognumber' : values['txtCatalogNumber'],
                      'multispecimen' : values['chkMultiSpecimen'],
                      'taxonname'     : '"%s"'%taxonName,
                      'taxonnameid'   : getPrimaryKey('taxonname',taxonName,'fullname'),
                      'typestatusid'  : getPrimaryKey('typestatus',values['cbxTypeStatus']),
                      'georegionname' : '"%s"'%values['cbxGeoRegion'],
                      'georegionid'   : getPrimaryKey('georegion',values['cbxGeoRegion']),
                      'storagename'   : '"%s"'%values['cbxStorage'],
                      'storageid'     : getPrimaryKey('storage',values['cbxStorage']),
                      'preptypename'  : '"%s"'%values['cbxPrepType'],
                      'preptypeid'    : getPrimaryKey('preptype',values['cbxPrepType']),
                      'notes'         : '"%s"'%values['txtNotes'],
                      'collectionid'  : collectionId,
                      'username'      : '"%s"'%values['txtUserName'],
                      #'userid'        : getPrimaryKey('"%s"'%values['txtUserName'],'username'),
                      'workstation'   : '"%s"'%values['txtWorkStation'],
                      'datetime'      : '"%s"'%datetime.now(),
                     }
            print('updated row dict=', fields)

            if currentRecordID:
                print(recordIDbacktrack, ' row should be UPDATED')
                print('updated fields::: ', fields)


        if event == sg.WINDOW_CLOSED:
            break

    window.close()

#init(2)
""" TO DO:
    Restrict the characters allowed in an input element to digits and . or -
    Accomplished by removing last character input if not a valid character
    This link provides some ideas for input sanitazion https://github.com/PySimpleGUI/PySimpleGUI/issues/1119
    What if the taxon name is a new one (not in the taxon table)? Needs to be handled? 
        - Covered by ticket #68 
"""