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

#function for converting predefined table data into list for dropdownlist 
def getList(tablename, collectionid): return util.convert_dbrow_list(db.getRowsOnFilters(tablename,{'collectionid =':'%s'%collectionid}))

#function for fetching id (primary key) on name value 
def getPrimaryKey(tableName, name, field='name'): return db.getRowsOnFilters(tableName, {' name = ':'"%s"'%name})[0]['id'] # return db.getRowsOnFilters(tableName, {' %s = ':'"%s"'%(field, name)})[0]['id']

sg.theme('SystemDefault')
blueArea = '#99ccff'
greenArea = '#E8F4EA'
greyArea = '#BFD1DF'

defaultSize = (21,1)
#defaultSize is used to space all data entry element labels so that they line up.
font = ('Bahnschrift', 13)
element_size = (30,1)
# element_size is the width of all fields in the 'green area'
blue_size = (28,1)
# blue_size is the width of all fields in the 'blue area'

def init(collection_id):
    # Set collection id  
    collectionId = collection_id
    c = collection_id
    
    # TODO when taxonomic_groups becomes a table in SQLite
    taxonomicGroups = ['placeholder...']

    # Input elements (below) are stored in variables with brackets to make it easier to include and position in the frames
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
                         sg.Combo('', key='cbxTaxonName', size=(28,6), text_color='black', background_color='white', font=('Arial', 12), readonly=True, enable_events=True, pad=((5,0),(0,0))),]

    barcode = [sg.Text('Barcode:', size=defaultSize, background_color=blueArea, text_color='black', font=font),
               sg.InputText('', key='txtCatalogNumber', size=blue_size, text_color='black', background_color='white', font=('Arial', 12), enable_events=True),]

    layout_bluearea = [broadGeo, taxonInput, taxonomicPicklist, barcode,
        # button_frame,
        [sg.StatusBar('', relief=None, size=(32,1), background_color=blueArea), 
         sg.Button('SAVE', key="btnSave", button_color='seagreen'), 
         sg.StatusBar('', relief=None, size=(20,1), background_color=blueArea), 
         sg.Button('Go Back', key="btnBack", button_color='firebrick', pad=(120,0))]]

    loggedIn = [sg.Text('Logged in as:', size=defaultSize, background_color=greyArea, font=font), sg.Input(size=(24,1), background_color='white', text_color='black', readonly=True, key='txtUserName'),]

    institution_ = [sg.Text('Institution:', size=defaultSize, background_color=greyArea, font=font), sg.Input(size=(24,1), background_color='white', text_color='black', readonly=True, key="txtInstitution"),]

    collections =  [sg.Text('Collection:', size=defaultSize, background_color=greyArea, font=font), sg.Input(size=(24,1), background_color='white', text_color='black', readonly=True, key="txtCollection"),]

    work_station =  [sg.Text('Workstation:', size=defaultSize, background_color=greyArea, font=font), sg.Input(size=(24,1), background_color='white', text_color='black', readonly=True, key="txtWorkStation"),]

    settings_ = [sg.Text('Settings ', size=defaultSize, justification='center', background_color=greyArea, font=14), 
                 sg.Button('', image_filename='%soptions_gear.png'%currentpath, button_color=greyArea, key='btnSettings', border_width=0)]

    horizontal_line = [sg.Text("_______________" * 5, background_color=greyArea)] #horizontal line element hack
    layout_greyarea = [loggedIn, institution_, horizontal_line, collections, work_station, settings_, [sg.Button('LOG OUT', key="btnLogout", button_color='grey40')]]

    layout = [[sg.Frame('',  [[sg.Column(layout_greenarea, background_color=greenArea)]], size=(250,200), expand_x=True, expand_y=True, background_color=greenArea),
               sg.Frame('', [[sg.Column(layout_greyarea, background_color=greyArea)]], size=(250, 300), expand_x=True, expand_y=True, background_color=greyArea)],
              [sg.Frame('',   [[sg.Column(layout_bluearea, background_color=blueArea)]], expand_x=True, expand_y=True, background_color=blueArea, title_location=sg.TITLE_LOCATION_TOP)],]

    collectionId = collection_id

    window = sg.Window("Mass Annotated Digitization Desk  (MADD)", layout, margins=(2, 2), size=(950,580), resizable=True, finalize=True )
    window['cbxTaxonName'].bind("<Return>", "_Enter")
    #The three lines below are there to ensure that the cursor in the input text fields is visible. It is invisible against a white background.
    # window['txtNotes'].Widget.config(insertbackground='black', highlightcolor='firebrick', highlightthickness=2)
    # window['txtUserName'].Widget.config(insertbackground='black', highlightcolor='firebrick', highlightthickness=2)

    #window['-TAXNAMES-'].Widget.config(insertbackground='black') , highlightcolor='firebrick', highlightthickness=2)

    # Set session Widget fields
    window.Element('txtUserName').Update(value=gs.spUserName) 
    collection = db.getRowOnId('collection', collection_id)
    if collection is not None:
        window.Element('txtCollection').Update(value=collection[2]) 
        institution = db.getRowOnId('institution', collection[3])
        window.Element('txtInstitution').Update(value=institution[2]) 
    window.Element('txtWorkStation').Update(value='TRS-80') 

    currrent_selection_index = 0
    window.Element('cbxTaxonName').Update(set_to_index=0)     # start with first item highlighted
    while True:
        event, values = window.read()
        # print('---', event, values)
        taxon_candidates = None
        listbox_values = ['','','']
        try: 
            if 'Up' in event or '16777235' in event:
                currrent_selection_index = (currrent_selection_index - 1) % len(listbox_values)
                window.Element('cbxTaxonName').Update(set_to_index=currrent_selection_index)
            elif 'Down' in event or '16777237' in event:
                cur_index = window.Element('selected_value').Widget.curselection()
                cur_index = (cur_index[0] + 1) % window.Element('selected_value').Widget.size()
                window.Element('cbxTaxonName').Update(set_to_index=cur_index)
                window.Element('cbxTaxonName').Update(scroll_to_index=cur_index)
                window.write_event_value('txtTaxonName', [window.Element('cbxTaxonName').GetListValues()[cur_index]])
        except:
            print('An error occurred')

        # Checking field events as switch construct 
        if event == 'cbxStorage':
            print('event:', event)
            print('In storage domain')
        if event == 'cbxPrepType':
            print('In preparation type')
            prepper = values[event]
            print('chosen isss: ', prepper)
        if event == 'cbxHigherTaxon':
            print('IN taxonomy section')
        if event == 'cbxTypeStatus':
            print('IN type status section')
        if event == 'txtNotes':
            print('IN notes section')
        if event == 'txtTaxonName':
            input_ = values['txtTaxonName']
            print('in taxon input -')
            print('len string : ', len(values[event]))

            if len(values[event]) >= 2:
                print('submitted string: ', values[event])
                response = koss.auto_suggest_taxonomy(values[event])
                # if response and response[1] <= 20: # obsolete filtering of results by list length
                if response is not None:
                    print('Suggested taxa based on input:) -- ', response)
                    window['cbxTaxonName'].update(values=response)
                    #     taxonomic_candidates_popup('Candidate names', response)
        if event == 'cbxTaxonName':
            selection = values[event]
            if selection:
                # item = selection[0]
                item = selection[0]
                # index = listbox.get_indexes()[0]
                # print(f'"{item}" selected')
        elif event == "cbxTaxonName" + "_Enter":
            print(event, values)
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
                      #'taxonnameid'   : getPrimaryKey('taxonname',taxonName,'fullname'),
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

        if event == sg.WINDOW_CLOSED:
            break
    window.close()

#init(2)

#def taxonomic_candidates_popup(title, names):
#     # This is the window where taxonomic candidate names appear to be selected by the operator
#     # title: is the string going into the window bar
#     # names: are the taxonomic names submitted by the initial DB query
#     names = list(names)
#     print(names)
#     layout = [
#         [sg.Listbox(names, size=(50, 20), font=("Courier New", 16), enable_events=True, key="-LISTBOX-")],
#         [sg.StatusBar("", size=(30, 1), key='-STATUS-')],
#     ]
#     #
#     # window = sg.Window(title, layout, finalize=True)
#     # listbox, status = window['-LISTBOX-'], window['-STATUS-']
#
#     while True:
#
#         event, values = window.read()
#         if event == sg.WIN_CLOSED or event == 'Exit':
#             break
#         elif event == '-LISTBOX-':
#             selection = values[event]
#             if selection:
#                 item = selection[0]
#                 # index = listbox.get_indexes()[0]
#                 print(f'"{item}" selected')
#                 # break
#
#                 window.close()
#         elif event == '-EXIT-':
#             window.close()

""" TO DO:
    Restrict the characters allowed in an input element to digits and . or -
    Accomplished by removing last character input if not a valid character
    This link provides some ideas for input sanitazion https://github.com/PySimpleGUI/PySimpleGUI/issues/1119
"""