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
import sqlite3
import sys
import pathlib
from datetime import datetime
import PySimpleGUI as sg
import tkinter as tk

# internal dependencies
import util
import data_access as db
import global_settings as gs
import home_screen as hs
import kick_off_sql_searches as koss
from saveOrInsert_functionGUI import saving_to_db
import data_exporter as dx
# import saveOrInsert_functionGUI as saver

# Make sure that current folder is registrered to be able to access other app files

sys.path.append(str(pathlib.Path(__file__).parent.parent.joinpath('MassDigitizer')))
currentpath = os.path.join(pathlib.Path(__file__).parent, '')

collectionId = -1
selectionIndex = 0
global indexer
indexer = []


def taxonomic_autosuggest_gui(partialName):

    # The list of choices that are going to be searched
    # In this example, the PySimpleGUI Element names are used
    choices = koss.auto_suggest_taxonomy(partialName)
    print(type(choices))

    print('len of choices is; ', len(choices), type(choices), '\n choices are;; ', choices)
    # sorted([elem.__name__ for elem in sg.Element.__subclasses__()])
    # choices =

    input_width = 20
    num_items_to_show = 4

    layout = [

        [sg.Text('Input Name:')],
        [sg.Input(size=(input_width, 1), enable_events=True, key='-IN-')],
        [sg.pin(
            sg.Col([[sg.Listbox(values=[], size=(input_width, num_items_to_show), enable_events=True, key='-BOX-',
                                select_mode=sg.LISTBOX_SELECT_MODE_SINGLE)]],
                   key='-BOX-CONTAINER-', pad=(0, 0), visible=True))],

    ]

    window = sg.Window('AutoComplete', layout, return_keyboard_events=True, finalize=True, modal=False,
                       font=('Helvetica', 16))
    # The parameter "modal" is explicitly set to False. If True the auto close behavior
    # won't work.

    list_element: sg.Listbox = window.Element(
        '-BOX-')  # store listbox element for easier access and to get to docstrings
    prediction_list, input_text, sel_item = choices, "", 0
    window['-IN-'].update(partialName)
    window.write_event_value('-IN-', partialName)
    # global windowAutosuggest
    # windowAutosuggest = window

    while True:  # Event Loop

        win, event, values = sg.read_all_windows()
        # print(win.close_destroys_window)
        if event is None:
            print('EVENT  , NONE')
            break
        # pressing down arrow will trigger event -IN- then aftewards event Down:40
        elif event.startswith('Escape'):
            window['-IN-'].update('')
            window['-BOX-CONTAINER-'].update(visible=False)
        elif event.startswith('Down') and len(prediction_list):
            sel_item = (sel_item + 1) % len(prediction_list)
            list_element.update(set_to_index=sel_item, scroll_to_index=sel_item)
        elif event.startswith('Up') and len(prediction_list):
            sel_item = (sel_item + (len(prediction_list) - 1)) % len(prediction_list)
            list_element.update(set_to_index=sel_item, scroll_to_index=sel_item)
        elif event == '\r':
            print('pressed Enter/Return')
            window.Hide()
            if len(values['-BOX-']) > 0:
                boxVal = values['-BOX-']
                print('boxval ISS - ', boxVal[0])
                window['-IN-'].update(value=boxVal[0])
                window['-BOX-CONTAINER-'].update(visible=False)
                return boxVal[0]

        elif event == '-IN-':
            # this concerns all keystrokes except the above ones.
            text = values['-IN-'].lower()
            if text == input_text:
                continue
            else:
                input_text = text

            prediction_list = []
            if len(text) >= 3:
                # condition for activating the autosuggest feature.
                prediction_list = [item for item in choices if item.lower().find(text) != -1]

            list_element.update(values=prediction_list)
            sel_item = 0
            list_element.update(set_to_index=sel_item)

            if len(prediction_list) > 0:
                window['-BOX-CONTAINER-'].update(visible=True)
            else:
                window['-BOX-CONTAINER-'].update(visible=False)
        elif event == '-BOX-':
            window['-IN-'].update(value=values['-BOX-'])
            window['-BOX-CONTAINER-'].update(visible=False)

    window.close()

def getList(tablename, collectionid): return util.convert_dbrow_list(
    db.getRowsOnFilters(tablename, {'collectionid =': '%s' % collectionid}))

# Function for fetching id (primary key) on name value
def getPrimaryKey(tableName, name, field='name'):
    return db.getRowsOnFilters(tableName, {' %s = ' % field: '"%s"' % name})[0]['id']

def init(collection_id):
    #

    # Set collection id
    collectionId = collection_id
    c = collection_id

    # Define UI areas
    sg.theme('SystemDefault')
    greenArea = '#E8F4EA'  # Stable fields
    blueArea = '#99ccff'  # Variable fields
    greyArea = '#BFD1DF'  # Session & Settings

    defaultSize = (21, 1)  # Ensure element labels are the same size so that they line up
    element_size = (30, 1)  # Default width of all fields in the 'green area'
    blue_size = (28, 1)  # Default width of all fields in the 'blue area'

    font = ('Bahnschrift', 13)
    element_keys = ['cbxStorage', 'cbxPrepType', 'cbxHigherTaxon', 'cbxTypeStatus', 'txtNotes', 'chkMultiSpecimen',
                    'cbxGeoRegion', 'txtTaxonName', 'cbxTaxonName', 'txtCatalogNumber', ]

    # TODO placeholder until higher taxonomic groups become available in SQLite
    taxonomicGroups = ['placeholder...']

    # Store elements in variables to make it easier to include and position in the frames
    storage = [sg.Text("Storage location:", size=defaultSize, background_color=greenArea, font=font),
               sg.Combo(getList('storage', c), key='cbxStorage', size=element_size, text_color='black',
                        background_color='white', font=('Arial', 12), readonly=True, enable_events=True), ]
    preparation = [sg.Text("Preparation type:", size=defaultSize, background_color=greenArea, font=font),
                   sg.Combo(getList('preptype', c), key='cbxPrepType', size=element_size, text_color='black',
                            background_color='white', font=('Arial', 12), readonly=True, enable_events=True), ]
    taxonomy = [sg.Text("Taxonomic group:", size=defaultSize, visible=False, background_color=greenArea, font=font),
                sg.Combo(taxonomicGroups, key='cbxHigherTaxon', visible=False, size=element_size, text_color='black',
                         background_color='white', font=('Arial', 12), readonly=True, enable_events=True), ]
    type_status = [sg.Text('Type status:', size=defaultSize, background_color=greenArea, font=font),
                   sg.Combo(getList('typeStatus', c), key='cbxTypeStatus', size=element_size, text_color='black',
                            background_color='white', font=('Arial', 12), readonly=True, enable_events=True), ]
    notes = [sg.Text('Notes', size=defaultSize, background_color=greenArea, font=font),
             sg.Multiline(size=(31, 5), background_color='white', text_color='black', key='txtNotes',
                          enable_events=False)]
    layout_greenarea = [storage, preparation, taxonomy, type_status, notes,
                        [sg.Checkbox('Multispecimen sheet', key='chkMultiSpecimen', background_color=greenArea,
                                     font=(11))], ]
    broadGeo = [
        sg.Text('Broad geographic region:', size=defaultSize, background_color=blueArea, text_color='black', font=font),
        sg.Combo(getList('georegion', c), size=blue_size, key='cbxGeoRegion', text_color='black',
                 background_color='white', font=('Arial', 12), readonly=True, enable_events=True), ]
    taxonInput = [
        sg.Text('Taxonomic name:     ', size=(21, 1), background_color=blueArea, text_color='black', font=font),
        sg.Input('', size=blue_size, key='txtTaxonName', text_color='black', background_color='white',
                 font=('Arial', 12), enable_events=True, pad=((5, 0), (0, 0))), ]

    taxonomicPicklist = [sg.Text('', size=defaultSize, background_color=blueArea, text_color='black', font=font),
                         sg.Listbox('', key='cbxTaxonName', select_mode=sg.LISTBOX_SELECT_MODE_BROWSE, size=(28, 6),
                                    text_color='black', background_color='white', font=('Arial', 12),
                                    bind_return_key=True, enable_events=True, pad=((5, 0), (0, 0))), 
                        ]
    barcode = [sg.Text('Barcode:', size=defaultSize, background_color=blueArea, enable_events=True, text_color='black', font=font),
               sg.InputText('', key='txtCatalogNumber', size=blue_size, text_color='black', background_color='white', font=('Arial', 12), enable_events=True),
               ]
    # statusLabel = [sg.Text('Specimen record has been saved', font=('Arial',20),size=(20,10),justification='center',background_color='#4f280a',text_color = 'yellow',key='texto')]
    lblExport = [sg.Text('', key='lblExport', visible=False, size=(100,2)), ]

    layout_bluearea = [broadGeo, taxonInput, taxonomicPicklist, barcode, 
                        
                       [sg.Text('Record ID: ', key='lblRecordID', background_color='#99dcff', visible=True,
                                size=(9, 1)),
                        sg.Text('', key='txtRecordID', size=(4,1), background_color=blueArea),
                        sg.StatusBar('', relief=None, size=(7, 1), background_color=blueArea),
                        sg.Button('SAVE', key="btnSave", button_color='seagreen', size=9, bind_return_key=True),
                        sg.StatusBar('', relief=None, size=(14, 1), background_color=blueArea),
                        sg.Button('Go Back', key="btnBack", button_color='firebrick', pad=(13, 0)),
                        sg.Text('Beginning of the name list reached. No more Go-back!', visible=False, key='lblWarning',
                                background_color="#ff5588", border_width=3),
                        sg.Button('Clear form', key='btnClear', button_color='black on white'),
                        sg.Button('Export data', key='btnExport', button_color='blue'),
                        sg.Button('Dismiss', key='btnDismiss', button_color='white on black'),
                        ],
                        lblExport
                       ]
    loggedIn = [sg.Text('Logged in as:', size=defaultSize, background_color=greyArea, font=font),
                sg.Input(disabled=True, size=(24, 1), background_color='white', text_color='black',
                         readonly=True, key='txtUserName'), ]
    institution_ = [sg.Text('Institution:', size=defaultSize, background_color=greyArea, font=font),
                    sg.Input(size=(24, 1), background_color='white', text_color='black',
                             readonly=True, key="txtInstitution"), ]
    collections = [sg.Text('Collection:', size=defaultSize, background_color=greyArea, font=font),
                   sg.Input(size=(24, 1), background_color='white', text_color='black',
                            readonly=True, key="txtCollection"), ]
    work_station = [sg.Text('Workstation:', size=defaultSize, background_color=greyArea, font=font),
                    sg.Input(size=(24, 1), background_color='white', text_color='black',
                             readonly=True, key="txtWorkStation"), ]
    # settings_ = [sg.Text('Settings ', size=defaultSize, justification='center', background_color=greyArea, font=14),
    #              sg.Button('', image_filename='%soptions_gear.png' % currentpath, key='btnSettings',
    #                        button_color=greyArea, border_width=0)]
    horizontal_line = [sg.Text("_______________" * 5, background_color=greyArea)]  # horizontal line element hack
    layout_greyarea = [loggedIn, institution_, horizontal_line, collections, work_station,
                       # settings_,
                       [sg.Button('LOG OUT', key="btnLogout", button_color='grey40')]]

    # Combine elements into full layout
    layout = [[sg.Frame('', [[sg.Column(layout_greenarea, background_color=greenArea)]], size=(250, 200), expand_x=True,
                        expand_y=True, background_color=greenArea),
               sg.Frame('', [[sg.Column(layout_greyarea, background_color=greyArea)]], size=(250, 300), expand_x=True,
                        expand_y=True, background_color=greyArea)],
              [sg.Frame('', [[sg.Column(layout_bluearea, background_color=blueArea)]], expand_x=True, expand_y=True,
                        background_color=blueArea, title_location=sg.TITLE_LOCATION_TOP)], ]

    window = sg.Window("Mass Annotated Digitization Desk  (MADD)", layout, margins=(2, 2), size=(960, 640),
                       resizable=True, return_keyboard_events=True, finalize=True)
    window.TKroot.focus_force()
    window['txtNotes'].bind('<Tab>', '+TAB')
    window['cbxTaxonName'].bind("<Return>", "_Enter")
    window['chkMultiSpecimen'].bind("<Return>", "_Enter")
    window.Element('txtUserName').Widget.config(takefocus=0)
    window.Element('txtInstitution').Widget.config(takefocus=0)
    window.Element('txtCollection').Widget.config(takefocus=0)
    window.Element('txtWorkStation').Widget.config(takefocus=0)
    # window.Element('btnSettings').Widget.config(takefocus=0)
    window.Element('btnLogout').Widget.config(takefocus=0)

    entry_barcode = window['txtCatalogNumber']
    entry_barcode.bind("<Return>", "_RETURN")
    #

    def getRecordIDbyBacktracking(backtrackCounter):
        # TODO must be reworked to use SQL statements rather than "counters" which rely on sequential IDs!
        sql = "select * from specimen s order by s.id DESC LIMIT {},1;".format(backtrackCounter)
        print('the SQL: ', sql)
        try:
            rows = db.executeSqlStatement(sql)
        except sqlite3.OperationalError:
            window['txtTaxonName'].update("Beginning of taxon names reached.")

        if rows:
            print('COUNTER row::::', rows[0])
            recordIDcurrent = rows[0]['id']
            return recordIDcurrent
        else:
            print('IN else clause due to no more GO_BACK !!')

            window['btnBack'].update(disabled=True)
            # window['lblWarning'].update(visible=True)

            backtrackCounter = backtrackCounter - 1
            sql = "select * from specimen s  order by s.id DESC LIMIT {},1;".format(backtrackCounter)
            rows = db.executeSqlStatement(sql)

        sql = "select * from specimen s  order by s.id DESC LIMIT {},1;".format(backtrackCounter)

        rows = db.executeSqlStatement(sql)
        if len(rows) > 0:
            print('COUNTER row::::', rows[0])
            recordIDcurrent = rows[0]['id']
        else :
            recordIDcurrent = 0

        return recordIDcurrent

    onecrementor = 0
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

    while True:
        event, values = window.read()
        def clear_all_of(fieldKeys):
            for key in fieldKeys:
                print(key)
                window[key].update('')

        # Checking field events as switch construct
        if event is None: break # Empty event indicates user closing window  
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
            print('tabbing!!!')
            window['chkMultiSpecimen'].set_focus()

        if event == 'chkMultiSpecimen_Enter':
            print('Multi specimen herbarium sheet was set to TRUE')
            window['chkMultiSpecimen'].update(True)
            window['cbxGeoRegion'].set_focus()

        if event == 'txtTaxonName':
            partialName = values['txtTaxonName']
            print('in taxon input -')
            # print('len string : ', len(values[event]))
            if len(values[event]) >= 3:

                print('submitted string: ', values[event])
                response = koss.auto_suggest_taxonomy(values[event])
                if response is not None:
                    print('Suggested taxa based on input:) -- ', response)
                    res = taxonomic_autosuggest_gui(partialName)
                    print('RESs is :: ', res)
                    window['txtTaxonName'].update(res)
                    window['txtCatalogNumber'].set_focus()

                    # window['cbxTaxonName'].update(set_to_index=[0], scroll_to_index=0)

        elif event == "cbxTaxonName" + "_Enter":  # For arrowing down to relevant taxon name and pressing Enter
            window['txtTaxonName'].update(values['cbxTaxonName'][0])
            print(f"InputTax: {values['cbxTaxonName'][0]}")
            window['cbxTaxonName'].update([])

        if event == "txtCatalogNumber_RETURN":
            print('vals= ', values)
            print(f"Input barcode yowsa: {values['txtCatalogNumber']}")
            window['btnSave'].set_focus()

        # Save form
        if values:
            taxonName = values['txtTaxonName']
            # for item in taxonName: unpackedTaxonName = item
            print('txtTaxonName bist: : ', taxonName)

        if event == 'btnSave':
            fields = {'catalognumber': '"%s"' % values['txtCatalogNumber'],
                      'multispecimen': values['chkMultiSpecimen'],
                      'taxonname': '"%s"' % taxonName,
                      'taxonnameid': getPrimaryKey('taxonname', taxonName, 'fullname'),
                      'typestatusid': getPrimaryKey('typestatus', values['cbxTypeStatus']),
                      'georegionname': '"%s"' % values['cbxGeoRegion'],
                      'georegionid': getPrimaryKey('georegion', values['cbxGeoRegion']),
                      #'storagefullname': '"%s"' % values['lblStorage'],
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

            existTable = db.getRows('specimen', limit=1)
            recordIDlabel = window['txtRecordID'].get()
            print('recordIDlabel:;: ', recordIDlabel)
            if existTable and not recordIDlabel:
                print('TTable existsss and no recordID operational<<')
                existResult = [j for j in existTable[0]]
                print("THE existing rec ///", existResult)
                res = saving_to_db(fields, insert=True)
                print('inserting roww :', res)
            elif recordIDlabel:
                print("we are in UPDATE mode")
                # print("! Empty tibble !")
                existingRecordID = recordIDlabel
                # recordID, via global dsRecordID, is here used to determine if a record is new, or if it is already existing
                print('pre existing id ...recordID == ', existingRecordID)

                # Checking if Save is a novel record , or if it is updating existing record.
                res = saving_to_db(fields, insert=False, recordID=existingRecordID)
                print('We are updating! ', res)
                clearingList = ['cbxStorage', 'cbxPrepType', 'cbxHigherTaxon', 'cbxTypeStatus', 'txtNotes',
                                'chkMultiSpecimen',
                                'cbxGeoRegion', 'txtTaxonName', 'cbxTaxonName', 'txtCatalogNumber']
                clear_all_of(clearingList)
                window['txtRecordID'].update('')


        if event == 'btnClear':
            clearingList = ['cbxStorage', 'cbxPrepType', 'cbxHigherTaxon', 'cbxTypeStatus', 'txtNotes',
                            'chkMultiSpecimen',
                            'cbxGeoRegion', 'txtTaxonName', 'cbxTaxonName', 'txtCatalogNumber']
            clear_all_of(clearingList)
            window['txtRecordID'].update('')

        if event == 'btnBack':
            print('Pressed go-back /')

            # Functionality for going back through the session records to make changes, or do checkups.
            currentRecordID = obtainTrack(incrementor=onecrementor)
            onecrementor += 1
            print('oneicrementor at -- ', onecrementor)
            print('current recordID :  ', currentRecordID)
            if not currentRecordID:
                window['txtTaxonName'].update("Beginning of taxon names reached.")
            else:
                rows = db.getRowOnId('specimen', currentRecordID)
                print('RAW row::::', rows[0])
                recordIDbacktrack = rows[0]
                dasRecordID = recordIDbacktrack
                print('record past ID : ', recordIDbacktrack)
                rowRecord = db.getRowOnId('specimen', currentRecordID)
                record = rowRecord

            print('the backtrack counter is now at: ', recordIDbacktrack)
            print('the ID of interest is= ', recordIDbacktrack)

            window['txtRecordID'].update('{}'.format(recordIDbacktrack), visible=True)
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

            fields = {'catalognumber': values['txtCatalogNumber'],
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
            print('updated row dict=', fields)

            if currentRecordID:
                print(recordIDbacktrack, ' row should be UPDATED')
                print('updated fields::: ', fields)

        if event == 'btnClear':
            clearingList = ['cbxStorage', 'cbxPrepType', 'cbxHigherTaxon', 'cbxTypeStatus', 'txtNotes',
                            'chkMultiSpecimen',
                            'cbxGeoRegion', 'txtTaxonName', 'cbxTaxonName', 'txtCatalogNumber']
            clear_all_of(clearingList)
            window['txtRecordID'].update('')
            window['lblExport'].update(visible=False)
            window['lblWarning'].update(visible=False)

        if event == 'btnExport':
            export_result = dx.exportSpecimens('xlsx')
            window['lblExport'].update(export_result,visible=True)

        if event == 'btnDismiss':
            window['lblExport'].update(visible=False)
            window['lblWarning'].update(visible=False)

        if event == sg.WINDOW_CLOSED:
            break

    window.close()



# gui_main(2)
#plz commit!!
""" TO DO:
    Restrict the characters allowed in an input element to digits and . or -
    Accomplished by removing last character input if not a valid character
    This link provides some ideas for input sanitazion https://github.com/PySimpleGUI/PySimpleGUI/issues/1119
    What if the taxon name is a new one (not in the taxon table)? Needs to be handled? 
        - Covered by ticket #68 
"""

