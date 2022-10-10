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

# TODO controller functions 
import kick_off_sql_searches as koss
from saveOrInsert_functionGUI import saving_to_db
# TODO model functions 
from models import specimen
import data_exporter as dx
# import saveOrInsert_functionGUI as saver

# Make sure that current folder is registrered to be able to access other app files
sys.path.append(str(pathlib.Path(__file__).parent.parent.joinpath('MassDigitizer')))
currentpath = os.path.join(pathlib.Path(__file__).parent, '')

collectionId = -1
selectionIndex = 0
global indexer
indexer = []
onecrementor = 0

window = None

# Specimen record 
collobj = None #specimen.specimen()

# Functional data
clearingList = ['cbxStorage', 'cbxPrepType', 'cbxHigherTaxon', 'cbxTypeStatus', 'txtNotes', 'chkMultiSpecimen', 'cbxGeoRegion', 'txtTaxonName', 'txtCatalogNumber'] #, 'cbxTaxonName']

def init(collection_id):
    # TODO function contract
    
    collobj = specimen.specimen(collection_id)
    print(len(collobj.storageLocations))

    # Define UI areas
    sg.theme('SystemDefault')
    greenArea = '#E8F4EA'  # Stable fields
    blueArea = '#99ccff'  # Variable fields
    greyArea = '#BFD1DF'  # Session & Settings

    defaultSize = (21, 1)  # Ensure element labels are the same size so that they line up
    element_size = (25, 1)  # Default width of all fields in the 'green area'
    green_size = (20, 1)  # Default width of all fields in the 'green area'
    blue_size = (35, 1)  # Default width of all fields in the 'blue area'

    font = ('Bahnschrift', 13)
    labelHeadlineMeta = ('Bahnschrift', 12)
    titleFont = ('Bahnschrift', 18)
    smallLabelFont = ('Arial', 11, 'italic')

    # TODO placeholder until higher taxonomic groups become available in SQLite
    taxonomicGroups = ['placeholder...']

    # Store elements in variables to make it easier to include and position in the frames
    storage = [
        sg.Text("Storage location:", size=defaultSize, background_color=greenArea, font=font),
        sg.Combo(util.convert_dbrow_list(collobj.storageLocations), key='cbxStorage', size=green_size, text_color='black',
                 background_color='white', font=('Arial', 12), readonly=True, enable_events=True),
        sg.Text("", key='txtStorageFullname', size=(50,2), background_color=greenArea, font=smallLabelFont)]    
    
    preparation = [
        sg.Text("Preparation type:", size=defaultSize, background_color=greenArea, font=font),
        sg.Combo(util.convert_dbrow_list(collobj.prepTypes), key='cbxPrepType', size=green_size, text_color='black',
                 background_color='white', font=('Arial', 12), readonly=True, enable_events=True), ]
    taxonomy = [
        sg.Text("Taxonomic group:", size=defaultSize, visible=False, background_color=greenArea, font=font),
        sg.Combo(taxonomicGroups, key='cbxHigherTaxon', visible=False, size=green_size, text_color='black',
                 background_color='white', font=('Arial', 12), readonly=True, enable_events=True), ]
    type_status = [
        sg.Text('Type status:', size=defaultSize, background_color=greenArea, font=font),
        sg.Combo(util.convert_dbrow_list(collobj.typeStatuses), key='cbxTypeStatus', size=green_size, text_color='black',
                 background_color='white', font=('Arial', 12), readonly=True, enable_events=True), ]
    notes = [
        sg.Text('Notes', size=defaultSize, background_color=greenArea, font=font),
        sg.InputText(size=(80, 5), key='txtNotes', background_color='white', text_color='black', enable_events=False)]

    layout_greenarea = [
        storage, preparation, taxonomy, type_status, notes,
        [sg.Checkbox('Multispecimen sheet', key='chkMultiSpecimen', background_color=greenArea,font=(11))], ] 

    broadGeo = [
        sg.Text('Broad geographic region:', size=defaultSize, background_color=blueArea, text_color='black', font=font),
        sg.Combo(util.convert_dbrow_list(collobj.geoRegions), size=blue_size, key='cbxGeoRegion', text_color='black',
                 background_color='white', font=('Arial', 12), readonly=True, enable_events=True), ]
    taxonInput = [
        sg.Text('Taxonomic name:     ', size=(21, 1), background_color=blueArea, text_color='black', font=font),
        sg.Input('', size=blue_size, key='txtTaxonName', text_color='black', background_color='white',
                 font=('Arial', 12), enable_events=True, pad=((5, 0), (0, 0))), ]
    # taxonomicPicklist = [
    #     sg.Text('', size=defaultSize, background_color=blueArea, text_color='black', font=font),
    #     sg.Listbox('', key='cbxTaxonName', select_mode=sg.LISTBOX_SELECT_MODE_BROWSE, size=(28, 6),
    #                text_color='black', background_color='white', font=('Arial', 12),
    #                bind_return_key=True, enable_events=True, pad=((5, 0), (0, 0))),]
    barcode = [
        sg.Text('Barcode:', size=defaultSize, background_color=blueArea, enable_events=True, text_color='black', font=font),
        sg.InputText('', key='txtCatalogNumber', size=blue_size, text_color='black', background_color='white', font=('Arial', 12), enable_events=True),]
    # statusLabel = [sg.Text('Specimen record has been saved', font=('Arial',20),size=(20,10),justification='center',background_color='#4f280a',text_color = 'yellow',key='texto')]
    lblExport = [sg.Text('', key='lblExport', visible=False, size=(100,2)), ]

    layout_bluearea = [broadGeo, taxonInput, barcode, [ # taxonomicPicklist, 
        sg.Text('Record ID: ', key='lblRecordID', background_color='#99dcff', visible=True, size=(9, 1)),
        sg.Text('', key='txtRecordID', size=(4,1), background_color=blueArea),
        sg.StatusBar('', relief=None, size=(7, 1), background_color=blueArea),
        sg.Button('SAVE', key="btnSave", button_color='seagreen', size=9, bind_return_key=True),
        sg.StatusBar('', relief=None, size=(14, 1), background_color=blueArea),
        sg.Button('GO BACK', key="btnBack", button_color='firebrick', pad=(13, 0)),
        sg.Text('Beginning of the name list reached. No more Go-back!', key='lblWarning', visible=False, background_color="#ff5588", border_width=3),
        sg.Button('GO FORWARDS', key='btnGoForward', button_color=('black','LemonChiffon2')),
        sg.Button('CLEAR FORM', key='btnClear', button_color='black on white'),
        #sg.Button('Export data', key='btnExport', button_color='royal blue'),  # Export data should be a backend feature says Pip 
        #sg.Button('Dismiss', key='btnDismiss', button_color='white on black'), # Notifications not needed says Pip
        ], lblExport ]

    loggedIn = [
        sg.Text('Logged in as:', size=(14,1), background_color=greyArea, font=labelHeadlineMeta),
        sg.Text(gs.spUserName, key='txtUserName', size=(25,1), background_color=greyArea, text_color='black', font=smallLabelFont),]
    institution_ = [
        sg.Text('Institution: ', size=(14,1), background_color=greyArea, font=labelHeadlineMeta),
        sg.Text(gs.institutionName, key='txtInstitution', size=(29,1), background_color=greyArea, font=smallLabelFont) ]
    collection = [
        sg.Text('Collection:', size=(14, 1), background_color=greyArea, text_color='black', font=labelHeadlineMeta),
        sg.Text(gs.collectionName, key='txtCollection', size=(25, 1), background_color=greyArea, font=smallLabelFont) ]
    workStation = [
        sg.Text('Workstation:', key="txtWorkStation", size=(14,1), background_color=greyArea, font=labelHeadlineMeta),
        sg.Text('', size=(20, 1), background_color=greyArea, text_color='black'), ]
    #settings_ = [sg.Text('Settings ', size=defaultSize, justification='center', background_color=greyArea, font=14),
    #             sg.Button('', image_filename='%soptions_gear.png' % currentpath, key='btnSettings', button_color=greyArea, border_width=0)]

    # Header section
    appTitle = sg.Text('Mass Annotation Digitization Desk (MADD)', size=(34, 3), background_color=greyArea, font=titleFont)
    settingsButton = sg.Button('SETTINGS', key='btnSettings', button_color='grey30')
    logoutButton = sg.Button('LOG OUT', key='btnLogOut', button_color='grey10')
    layoutTitle = [[appTitle],]
    layoutSettingLogout = [sg.Push(background_color=greyArea), settingsButton, logoutButton]
    layoutMeta = [loggedIn, institution_, collection, workStation, layoutSettingLogout]

    # Combine elements into full layout - the first frame group is the grey metadata area.
    layout = [[
        sg.Frame('', layoutTitle, size=(550, 100), pad=(0,0), background_color=greyArea, border_width=0),
        sg.Frame('',  layoutMeta, size=(500,120), pad=(0,0), border_width=0, background_color=greyArea)],
        [sg.Frame('', [[sg.Column(layout_greenarea, background_color=greenArea)]], size=(250, 175), background_color=greenArea, expand_x=True, ),],#expand_y=True, 
        [sg.Frame('', [[sg.Column(layout_bluearea, background_color=blueArea)]], title_location=sg.TITLE_LOCATION_TOP, background_color=blueArea, expand_x=True, expand_y=True, )], ]#
    
    window = sg.Window("Mass Annotated Digitization Desk  (MADD)", layout, margins=(2, 2), size=(960, 480), resizable=True, return_keyboard_events=True, finalize=True, background_color=greyArea)
    
    window.TKroot.focus_force()

    # Set session fields
    window.Element('txtUserName').Update(value=gs.spUserName)
    collection = db.getRowOnId('collection', collection_id)
    if collection is not None:
        window.Element('txtCollection').Update(value=collection[2])
        institution = db.getRowOnId('institution', collection[3])
        window.Element('txtInstitution').Update(value=institution[2])
    window.Element('txtWorkStation').Update(value='TRS-80')

    # Set control events 
    # Header area
    window.Element('btnSettings').Widget.config(takefocus=0)
    window.Element('btnLogOut').Widget.config(takefocus=0)
    window.Element('txtUserName').Widget.config(takefocus=0)
    # Green area 
    #cbxStorage 
    #cbxPrepType 
    #cbxTypeStatus 
    window['txtNotes'].bind('<Tab>', '+TAB')
    window['txtNotes'].bind('<Leave>', '_Edit')
    window['chkMultiSpecimen'].bind("<Leave>", "_Edit")
    window['chkMultiSpecimen'].bind("<Return>", "_Enter")
    # Blue area     
    #cbxGeoRegion    
    #window['cbxTaxonName'].bind("<Return>", "_Enter")
    window['txtCatalogNumber'].bind('<Leave>', '_Edit')    
    entry_barcode = window['txtCatalogNumber']
    entry_barcode.bind("<Return>", "_RETURN")

    # Loop through GUI events
    while True:
        event, values = window.read()

        # Checking field events as switch construct
        if event is None: break # Empty event indicates user closing window  

        if event == 'cbxStorage':
            collobj.setStorageFields(window[event].widget.current())
            window['txtStorageFullname'].update(collobj.storageFullname)
            
        if event == 'cbxPrepType':
            collobj.setPrepTypeFields(window[event].widget.current())

        #if event == 'cbxHigherTaxon':
        #    pass
        
        if event == 'cbxTypeStatus':
            collobj.setTypeStatusFields(window[event].widget.current())
        
        if event == 'txtNotes_Edit':
            collobj.notes = values['txtNotes']
        
        if event.endswith('+TAB'):
            collobj.notes = values['txtNotes']
            window['chkMultiSpecimen'].set_focus()

        if event == 'chkMultiSpecimen_Enter':
            collobj.multiSpecimen = values[event]
            window['chkMultiSpecimen'].update(True)
            window['cbxGeoRegion'].set_focus()

        if event == 'txtCatalogNumber':
            collobj.catalogNumber = values[event]

        if event == 'txtCatalogNumber_Edit':
            collobj.catalogNumber = values['txtCatalogNumber']

        if event == "txtCatalogNumber_RETURN":
            collobj.catalogNumber = values['txtCatalogNumber']
            window['btnSave'].set_focus()
        
        if event == 'chkMultiSpecimen_Edit': 
            collobj.multiSpecimen = values['chkMultiSpecimen']

        if event == 'cbxGeoRegion':
            collobj.setgeoRegionFields(window[event].widget.current())
        
        if event == 'txtTaxonName':
            partialName = values['txtTaxonName']
            if len(values[event]) >= 3:
                #print('submitted string: ', values[event])
                response = koss.auto_suggest_taxonomy(values[event])
                if response is not None:
                    print('Suggested taxa based on input:) -- ', response)
                    # TODO OUTCOMMENTED THIS BECAUSE IT STARTED TO GIVE ERRORS AND
                    #      IT WILL BE WIRED THROUGH THE GENERIC AUTOSUGGEST ANYWAY
                    #res = taxonomic_autosuggest_gui(partialName)
                    #window['txtTaxonName'].update(res)
                    #collobj.taxonName = res
                    window['txtCatalogNumber'].set_focus()
                    # window['cbxTaxonName'].update(set_to_index=[0], scroll_to_index=0)

        # elif event == "cbxTaxonName" + "_Enter":  # For arrowing down to relevant taxon name and pressing Enter
        #     window['txtTaxonName'].update(values['cbxTaxonName'][0])
        #     print(f"InputTax: {values['cbxTaxonName'][0]}")
        #     window['cbxTaxonName'].update([])

        if event == 'btnClear':
            clear_all_of(window)
            window['txtRecordID'].update('')

        if event == 'btnBack':
            # TODO handle in specimen class 
            print('Pressed go-back /')
            global  onecrementor
            # Functionality for going back through the session records to make changes, or do checkups.
            currentRecordID = collobj.obtainTrack(incrementor=onecrementor)
            onecrementor += 1
            print('oneicrementor at -- ', onecrementor)
            #print('current recordID :  ', currentRecordID)
            if not currentRecordID:
                window['txtTaxonName'].update("Beginning of taxon names reached.")
            else:
                rows = db.getRowOnId('specimen', currentRecordID)
                #print('RAW row::::', rows[0])
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
            #window['cbxTaxonName'].update([])
            window['txtCatalogNumber'].update(record['catalognumber'])

            if currentRecordID:
                print(recordIDbacktrack, ' row should be UPDATED')

        if event == 'btnClear':
            clear_all_of(window)
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
        
        # Save form
        if values:
            pass

        if event == 'btnSave':

            # TODO explain code 
            if collobj.id >= 0:
                clear_all_of(window)
                window['txtRecordID'].update('')
            
            previousId = collobj.save()
            collobj = specimen.specimen(collection_id)
            collobj.previousId = previousId

    window.close()

# TODO explain the function of below lines 
def clear_all_of(win):
    for key in clearingList:
        print(key)
        win[key].update('')

def taxonomic_autosuggest_gui(partialName):
    # TODO Function contract 
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
            sg.Col([[sg.Listbox(values=[], size=(input_width, num_items_to_show), enable_events=True, key='-BOX-', select_mode=sg.LISTBOX_SELECT_MODE_SINGLE)]],
                   key='-BOX-CONTAINER-', pad=(0, 0), visible=True))],]

    window = sg.Window('AutoComplete', layout, return_keyboard_events=True, finalize=True, modal=False, font=('Helvetica', 16))
    # The parameter "modal" is explicitly set to False. If True the auto close behavior won't work.

    list_element: sg.Listbox = window.Element('-BOX-')  # store listbox element for easier access and to get to docstrings
    prediction_list, input_text, sel_item = choices, "", 0
    window['-IN-'].update(partialName)
    window.write_event_value('-IN-', partialName)
    # global windowAutosuggest
    # windowAutosuggest = window

    while True:  # Event Loop
        
        event, values = sg.read_all_windows()
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
            # A patch on the issue around the popup not being closed properly.
            # Likely to be a PySimpleGUI bug.
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


""" TO DO:
    Restrict the characters allowed in an input element to digits and . or -
    Accomplished by removing last character input if not a valid character
    This link provides some ideas for input sanitazion https://github.com/PySimpleGUI/PySimpleGUI/issues/1119
    What if the taxon name is a new one (not in the taxon table)? Needs to be handled? 
        - Covered by ticket #68 
"""

