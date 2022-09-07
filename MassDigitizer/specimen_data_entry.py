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

# Function for converting predefined table data into list for dropdownlist 
def getList(tablename, collectionid): return util.convert_dbrow_list(db.getRowsOnFilters(tablename,{'collectionid =':'%s'%collectionid}))

# Function for fetching id (primary key) on name value 
def getPrimaryKey(tableName, name, field='name'): return db.getRowsOnFilters(tableName, {' %s = '%field : '"%s"'%name})[0]['id'] # return db.getRowsOnFilters(tableName, {' %s = ':'"%s"'%(field, name)})[0]['id']

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
    taxonomy = [sg.Text("Taxonomic group:", size=defaultSize, background_color=greenArea, font=font),
                sg.Combo(taxonomicGroups, key='cbxHigherTaxon', size=element_size, text_color='black', background_color='white', font=('Arial', 12), readonly=True, enable_events=True),]
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
                         sg.Listbox('', key='cbxTaxonName', select_mode='browse', size=(28, 6), text_color='black', background_color='white', font=('Arial', 12), enable_events=True, pad=((5, 0), (0, 0))), ]
    barcode = [sg.Text('Barcode:', size=defaultSize, background_color=blueArea, enable_events=True, text_color='black', font=font),
               sg.InputText('', key='txtCatalogNumber', size=blue_size, text_color='black', background_color='white', font=('Arial', 12), enable_events=True),]
    # statusLabel = [sg.Text('Specimen record has been saved', font=('Arial',20),size=(20,10),justification='center',background_color='#4f280a',text_color = 'yellow',key='texto')]


    layout_bluearea = [broadGeo, taxonInput, taxonomicPicklist, barcode,

        [sg.StatusBar('', relief=None, size=(32,1), background_color=blueArea), 
         sg.Button('SAVE', key="btnSave", button_color='seagreen', bind_return_key=True),
         sg.StatusBar('', relief=None, size=(20,1), background_color=blueArea), 
         sg.Button('Go Back', key="btnBack", button_color='firebrick', pad=(120,0))]]
    loggedIn = [sg.Text('Logged in as:', size=defaultSize, background_color=greyArea, font=font), sg.Input(disabled=True, size=(24,1), background_color='white', text_color='black',
                readonly=True, key='txtUserName'),]
    institution_ = [sg.Text('Institution:', size=defaultSize, background_color=greyArea, font=font), sg.Input(size=(24,1), background_color='white', text_color='black', 
                readonly=True, key="txtInstitution"),]
    collections =  [sg.Text('Collection:', size=defaultSize, background_color=greyArea, font=font), sg.Input(size=(24,1), background_color='white', text_color='black', 
                readonly=True, key="txtCollection"),]
    work_station =  [sg.Text('Workstation:', size=defaultSize, background_color=greyArea, font=font), sg.Input(size=(24,1), background_color='white', text_color='black', 
                readonly=True, key="txtWorkStation"),]
    settings_ = [sg.Text('Settings ', size=defaultSize, justification='center', background_color=greyArea, font=14), 
                 sg.Button('', image_filename='%soptions_gear.png'%currentpath, button_color=greyArea, key='btnSettings', border_width=0)]
    horizontal_line = [sg.Text("_______________" * 5, background_color=greyArea)] # horizontal line element hack
    layout_greyarea = [loggedIn, institution_, horizontal_line, collections, work_station, settings_, [sg.Button('LOG OUT', key="btnLogout", button_color='grey40')]]

    # Combine elements into full layout
    layout = [[sg.Frame('',  [[sg.Column(layout_greenarea, background_color=greenArea)]], size=(250,200), expand_x=True, expand_y=True, background_color=greenArea),
               sg.Frame('', [[sg.Column(layout_greyarea, background_color=greyArea)]], size=(250, 300), expand_x=True, expand_y=True, background_color=greyArea)],
              [sg.Frame('',   [[sg.Column(layout_bluearea, background_color=blueArea)]], expand_x=True, expand_y=True, background_color=blueArea, title_location=sg.TITLE_LOCATION_TOP)],]

    window = sg.Window("Mass Annotated Digitization Desk  (MADD)", layout, margins=(2, 2), size=(950,580), resizable=True, return_keyboard_events=True, finalize=True )

    window['cbxTaxonName'].bind("<Return>", "_Enter")
    window['chkMultiSpecimen'].bind("<Return>", "_Enter")

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
    item = None

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
        if event.endswith('+TAB'):
            window['cbxGeoRegion'].set_focus()
        if event == 'chkMultiSpecimen_Enter':
            print('Multi specimen herbarium sheet was set to TRUE')
            window['chkMultiSpecimen'].update(True)
            window['cbxGeoRegion'].set_focus()
        if event == 'txtTaxonName':
            input_ = values['txtTaxonName']
            print('in taxon input -')
            print('len string : ', len(values[event]))
            if len(values[event]) >= 2:
                print('submitted string: ', values[event])
                response = koss.auto_suggest_taxonomy(values[event])
                if response is not None:
                    print('Suggested taxa based on input:) -- ', response)
                    window['cbxTaxonName'].update(values=response)
                    window['cbxTaxonName'].update(set_to_index=[0], scroll_to_index=0)
        #             Forces 1st item in list to be highlighted which makes it selectable by Return key

        if event == 'cbxTaxonName':
            index = 0 # Reset highlighted item 
            window['cbxTaxonName'].update(scroll_to_index=index)
            selection = values[event]
            print('selection ;', selection)
            if selection:
                item = selection[0]
                print('item at selection=', item)

        elif event == "cbxTaxonName" + "_Enter": # For arrowing down to relevant taxon name and pressing Enter
            window['txtTaxonName'].update(values['cbxTaxonName'][0])
            print(f"Input: {values['cbxTaxonName']}")
        if event == "txtCatalogNumber_RETURN":
            print('vals= ', values)
            print(f"Input barcode yowsa: {values['txtCatalogNumber']}")
            window['btnSave'].set_focus()

        if event == 'btnLogout':
            gs.clearSession()
            hs.window.reappear()
            window.close()

        # Save form 
        if event == 'btnSave':
            print('Saving form')

            taxonName = ''
            if len(values['cbxTaxonName']) > 0:
                taxonName = values['cbxTaxonName'][0]

            # pull data entered from form fields  
            fields = {'catalognumber' : '"%s"'%values['txtCatalogNumber'],
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
            
            print(fields)
            db.insertRow('specimen', fields)

            # reset/blank out elements that are NOT sticky
            window['cbxTypeStatus'].update([])
            window['cbxTaxonName'].update([])
            window['txtNotes'].update('')
            window['txtTaxonName'].update([])
            window['txtCatalogNumber'].update([])

        if event == sg.WINDOW_CLOSED:
            break
    window.close()

init(2)
""" TO DO:
    Restrict the characters allowed in an input element to digits and . or -
    Accomplished by removing last character input if not a valid character
    This link provides some ideas for input sanitazion https://github.com/PySimpleGUI/PySimpleGUI/issues/1119
    What if the taxon name is a new one (not in the taxon table)? Needs to be handled? 
        - Covered by ticket #68 
"""