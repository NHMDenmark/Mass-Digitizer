# -*- coding: utf-8 -*-
"""
Created on Thu May 26 17:44:00 2022

@author: Jan K. Legind, NHMD

Copyright 2022 Natural History Museum of Denmark (NHMD)

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing,
software distributed under the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND,
either express or implied. See the License for the specific language governing permissions and limitations under the License.
"""
from queue import Empty
import PySimpleGUI as sg
# import import_csv_memory
import util
import os
import sys
import pathlib

import data_access as db
import global_settings as gs
import home_screen as hs

sys.path.append(str(pathlib.Path(__file__).parent.parent.joinpath('MassDigitizer')))
currentpath = os.path.join(pathlib.Path(__file__).parent, '')
import kick_off_sql_searches as koss

sg.theme('SystemDefault')
blueArea = '#99ccff'
greenArea = '#E8F4EA'
greyArea = '#BFD1DF'

#Drop-down list parameters populated by DB queries
prepType = []
prep_objects = koss.small_list_lookup('preptype', 5)
for j in prep_objects:
    prepType_name = j['name']
    print(j['name'])
    prepType.append(prepType_name)
#TO BE DONE when taxonomic_groups becomes a table in SQLite
taxonomicGroups = ['placeholder...']
#END to-do

typeStatus = []
type_objects = koss.small_list_lookup('typestatus', 5)
for j in type_objects:
    type_name = j['name']
    print(j['name'])
    typeStatus.append(type_name)

institutions = []
storage_objects = koss.small_list_lookup('institution', 5)
for j in storage_objects:
    institution_name = j['name']
    print(j['name'])
    institutions.append(institution_name)

#Georegions /blue area below -v
geoRegionsCopenhagen = []
geo_objects = koss.small_list_lookup('georegion', 5)
for j in geo_objects:
    georegion_name = j['name']
    print(j['name'])
    geoRegionsCopenhagen.append(georegion_name)

# Hardcoded barcode
barcode = [58697014]

defaultSize = (21,1)
#defaultSize is used to space all data entry element labels so that they line up.
font = ('Bahnschrift', 13)
element_size = (30,1)
# element_size is the width of all fields in the 'green area'
blue_size = (28,1)
# blue_size is the width of all fields in the 'blue area'

#Input elements (below) are stored in variables with brackets to make it easier to include and position in the frames
storage = [sg.Text("Storage location:", size=defaultSize, background_color=greenArea, font=font),
           sg.Combo(institutions, key='cbxStorage', size=element_size, text_color='black', background_color='white', font=('Arial', 12), enable_events=True),]

preparation = [sg.Text("Preparation type:", size=defaultSize, background_color=greenArea, font=font),
               sg.Combo(prepType, key='cbxPrepType', size=element_size, text_color='black', background_color='white',font=('Arial', 12), enable_events=True),]

taxonomy = [sg.Text("Taxonomic group:", size=defaultSize, background_color=greenArea, font=font),
            sg.Combo(taxonomicGroups, key='cbxHigherTaxon', size=element_size, text_color='black', background_color='white', font=('Arial', 12), enable_events=True),]

type_status = [sg.Text('Type status:', size=defaultSize, background_color=greenArea, font=font),
               sg.Combo(typeStatus, key='cbxTypeStatus', size=element_size, text_color='black', background_color='white', font=('Arial', 12), enable_events=True),]

notes = [sg.Text('Notes', size=defaultSize, background_color=greenArea, font=font),
         sg.Multiline(size=(31,5), background_color='white', text_color='black', key='txtNotes', enable_events=False)]

layout_greenarea = [storage, preparation, taxonomy, type_status, notes, [sg.Checkbox('Multispecimen sheet', background_color=greenArea, font=(11))],]

broadGeo = [sg.Text('Broad geographic region:', size=defaultSize ,background_color=blueArea, text_color='black', font=font),
            sg.Combo(geoRegionsCopenhagen, size=blue_size, key='cbxGeoRegion', text_color='black', background_color='white', font=('Arial', 12), enable_events=True),]

taxonInput = [sg.Text('Taxonomic name:     ', size=(21,1) ,background_color=blueArea, text_color='black', font=font),
              sg.Input('', size=blue_size, key='txtDetermination', text_color='black', background_color='white', font=('Arial', 12), enable_events=True, pad=((5,0),(0,0))),]

taxonomicPicklist = [sg.Text('', size=defaultSize, background_color=blueArea, text_color='black', font=font),
                    sg.Listbox('', key='cbxDetermination', size=(28,6), text_color='black', background_color='white', font=('Arial', 12), enable_events=True, pad=((5,0),(0,0))),]

barcode = [sg.Text('Barcode:', size=defaultSize, background_color=blueArea, text_color='black', font=font),
           sg.InputText('', key='txtCatalogNumber', size=blue_size, text_color='black', background_color='white', font=('Arial', 12), enable_events=True),]

# button_frame = [sg.Frame(layout=[[sg.Button('SAVE', key='-SAVE-', button_color='seagreen'), sg.StatusBar('', relief=None, size=(30,1), background_color=blueArea),
#                                   sg.Button('Go back', key='-GOBACK', button_color='firebrick'),
#         sg.Sizer(280, 10)]] , title='', relief=None, background_color=blueArea, border_width=0)]


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

def init(collection_id):
    window = sg.Window("Mass Annotated Digitization Desk  (MADD)", layout, margins=(2, 2), size=(950,580), resizable=True, finalize=True )
    #The three lines below are there to ensure that the cursor in the input text fields is visible. It is invisible against a white background.
    window['txtNotes'].Widget.config(insertbackground='black', highlightcolor='firebrick', highlightthickness=2)
    window['txtUserName'].Widget.config(insertbackground='black', highlightcolor='firebrick', highlightthickness=2)

    #window['-TAXNAMES-'].Widget.config(insertbackground='black')
                                   # , highlightcolor='firebrick', highlightthickness=2)

    # Set session Widget fields
    window.Element('txtUserName').Update(value=gs.spUserName) 
    collection = db.getRowOnId('collection', collection_id)
    if collection is not Empty:
        window.Element('txtCollection').Update(value=collection[2]) 
        institution = db.getRowOnId('institution', collection[3])
        window.Element('txtInstitution').Update(value=institution[2]) 
    window.Element('txtWorkStation').Update(value='TRS-80') 

    currrent_selection_index = 0
    window.Element('cbxDetermination').Update(set_to_index=0)     # start with first item highlighted
    while True:
        event, values = window.read()
        # print('---', event, values)
        taxon_candidates = None
        listbox_values = ['','','']
        try: 
            if 'Up' in event or '16777235' in event:
                currrent_selection_index = (currrent_selection_index - 1) % len(listbox_values)
                window.Element('cbxDetermination').Update(set_to_index=currrent_selection_index)
            elif 'Down' in event or '16777237' in event:
                cur_index = window.Element('selected_value').Widget.curselection()
                cur_index = (cur_index[0] + 1) % window.Element('selected_value').Widget.size()
                window.Element('cbxDetermination').Update(set_to_index=cur_index)
                window.Element('cbxDetermination').Update(scroll_to_index=cur_index)
                window.write_event_value('txtDetermination', [window.Element('cbxDetermination').GetListValues()[cur_index]])
        except:
            print('An error occurred')
            pass

        if event == 'txtDetermination':
            # window.Element('txtDetermination').Update(set_to_index=currrent_selection_index)
            pass
        #SWITCH CONSTRUCT
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
        if event == 'txtDetermination':
            input_ = values['txtDetermination']
            print('in taxon input -')
            print('len string : ', len(values[event]))

            if len(values[event]) >= 2:
                print('submitted string: ', values[event])
                response = koss.auto_suggest_taxonomy(values[event])
                # if response and response[1] <= 20:
                if response is not None:
                    print('the auto suggeter SAYS :) -- ', response[0])
                    window['cbxDetermination'].update(values=response[0])
                    #     taxonomic_candidates_popup('Candidate names', response[0])
        if event == 'txtDetermination':
            selection = values[event]
            if selection:
                item = selection[0]
                # index = listbox.get_indexes()[0]
                print(f'"{item}" selected')
        if event == 'btnLogout':
            gs.clearSession()
            hs.window.reappear()
            window.close()
        if event == sg.WINDOW_CLOSED:
            break
    window.close()

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

# init(2)

""" TO DO:
    Restrict the characters allowed in an input element to digits and . or -
    Accomplished by removing last character input if not a valid character
    This link provides some ideas for input sanitazion https://github.com/PySimpleGUI/PySimpleGUI/issues/1119
"""