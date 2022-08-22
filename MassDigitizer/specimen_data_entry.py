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
import PySimpleGUI as sg
# import import_csv_memory
import util
import os
import sys
import pathlib

sys.path.append(str(pathlib.Path(__file__).parent.parent.joinpath('MassDigitizer')))

currentpath = os.path.join(pathlib.Path(__file__).parent, '')
import kick_off_sql_searches as koss


sg.theme('Material2')
blueArea = '#99ccff'
greenArea = '#E8F4EA'
greyArea = '#BFD1DF'

#All hardcoded stuff are likely to be replaced by DB queries
institutions = ['NHMD: Natural History Museum of Denmark (Copenhagen)', 'NHMA: Natural History Museum Aarhus', 'TEST: Test server']
prepType = ['pinned', 'herbarium sheets']
taxonomicGroups = ['placeholder...']
typeStatus =  ['placeholder...']
#Georegions /blue area below -v
geoRegionsCopenhagen = ['Nearctic', 'Palearctic', 'Neotropical', 'Afrotropical', 'Oriental', 'Australian']
# taxonomicNames = ['Acanthohelicospora aurea','Acremonium alternatum','Actinonema actaeae','Aegerita alba','Agaricus aestivalis','Agaricus aestivalis var. flavotacta','Agaricus altipes']
barcode = [58697014]
#Grey area hardcoding below
collections = ['Botany', 'Entomology', 'Ichthyology']
workstations = ['Commodore_64', 'VIC_20', 'HAL2000', 'Cray']

defaultSize = (21,1)
#defaultSize is used to space all data entry elements so that they line up.
font = ('Bahnschrift', 13)
element_size = (30,1)
blue_size = (28,1)

#Input elements (below) are stored in variables with brackets to make it easier to include and position in the frames
storage = [
                    sg.Text("Storage location:", size=defaultSize, background_color=greenArea, font=font),
                    sg.Combo(institutions, key='-STORAGE-', size=element_size, text_color='black', background_color='white', font=('Arial', 12), enable_events=True),
                ]

preparation = [
                    sg.Text("Preparation type:", size=defaultSize, background_color=greenArea, font=font),
                    sg.Combo(prepType, key='-PREP-', size=element_size, text_color='black', background_color='white', enable_events=True),
                    ]

taxonomy = [
                    sg.Text("Taxonomic group:", size=defaultSize, background_color=greenArea, font=font),
                    sg.Combo(taxonomicGroups, key='-TAXON-', size=element_size, text_color='black', background_color='white', enable_events=True),
                    ]

type_status = [
                    sg.Text('Type status:', size=defaultSize, background_color=greenArea, font=font),
                    sg.Combo(typeStatus, key='-TYPE-', size=element_size, text_color='black', background_color='white', font=font, enable_events=True),
                 ]

notes = [sg.Text('Notes', size=defaultSize, background_color=greenArea, font=font),
         sg.Multiline(size=(29,5), background_color='white', text_color='black', key='-NOTES-', enable_events=False)]
# note_box = [sg.Multiline(size=(24,5), background_color='white', text_color='black', key='-NOTES-')]

layout_greenarea = [
    storage, preparation, taxonomy, type_status, notes, [sg.Checkbox('Multispecimen sheet', background_color=greenArea, font=(11))],
    ]
#Above is the so-called 'green area'

broadGeo = [
                    sg.Text('Broad geographic region:', size=defaultSize ,background_color=blueArea, text_color='black', font=font),
                    sg.Combo(geoRegionsCopenhagen, size=blue_size, key='-GEOREGION-', text_color='black', background_color='white', enable_events=True),
                 ]

taxonomicName = [
                    sg.Text('Taxonomic name:', size=defaultSize, background_color=blueArea, text_color='black', font=font),
                    sg.InputText('', key='-TAXNAMES-', size=blue_size, text_color='black', background_color='white', enable_events=True),
                 ]

barcode = [
                    sg.Text('Barcode:', size=defaultSize, background_color=blueArea, text_color='black', font=font),
                    sg.InputText('', key='-BARCODE-', size=blue_size, text_color='black', background_color='white', enable_events=True),
                 ]

# button_frame = [sg.Frame(layout=[[sg.Button('SAVE', key='-SAVE-', button_color='seagreen'), sg.StatusBar('', relief=None, size=(30,1), background_color=blueArea),
#                                   sg.Button('Go back', key='-GOBACK', button_color='firebrick'),
#         sg.Sizer(280, 10)]] , title='', relief=None, background_color=blueArea, border_width=0)]


layout_bluearea = [
    broadGeo, taxonomicName, barcode,
    # button_frame,
    [sg.StatusBar('', relief=None, size=(32,1), background_color=blueArea), sg.Button('SAVE', key="-SAVE-", button_color='seagreen'), sg.StatusBar('', relief=None, size=(20,1), background_color=blueArea), sg.Button('Go Back', key="-GOBACK-", button_color='firebrick', pad=(120,0))]
]

loggedIn = [sg.Text('Logged in as:', size=defaultSize, background_color=greyArea, font=font), sg.InputText(size=(24,1), background_color='white', text_color='black', key='-LOGGED-'),
         ]

dateTime = [sg.Text('Date / Time:', size=defaultSize, background_color=greyArea, font=font), sg.InputText(size=(24,1), background_color='white', text_color='black', key='-DATETIME-'),
         ]

institution_ = [sg.Text('Institution:', size=defaultSize, background_color=greyArea, font=font), sg.Combo(institutions, key="-INSTITUTION-", size=element_size, text_color='black', background_color='white'),
         ]

collections =  [sg.Text('Collection name:', size=defaultSize, background_color=greyArea, font=font), sg.Combo(collections, key="-COLLECTION-", size=element_size, text_color='black', background_color='white'),
         ]

work_station =  [sg.Text('Workstation:', size=defaultSize, background_color=greyArea, font=font), sg.Combo(workstations, key="-WORKSTATION-", size=element_size, text_color='black', background_color='white'),
         ]

settings_ = [sg.Text('Settings ', size=defaultSize, justification='center', background_color=greyArea, font=14), sg.Button('', image_filename='%soptions_gear.png'%currentpath,
                                                                                          button_color=greyArea, key='-SETTING-', border_width=0)
         ]


layout_greyarea = [loggedIn, dateTime, [sg.Text("_______________" * 5, background_color=greyArea)], institution_,
                   collections, work_station, settings_, [sg.Button('LOG OUT', key="-LOGOUT-", button_color='grey40')]]
#there is a hacky horizontal line element in the code above to create space between inputs

layout = [
    [sg.Frame('',  [[sg.Column(layout_greenarea, background_color=greenArea)]], size=(250,200), expand_x=True, expand_y=True, background_color=greenArea),
     sg.Frame('', [[sg.Column(layout_greyarea, background_color=greyArea)]], size=(250, 300), expand_x=True, expand_y=True, background_color=greyArea)],
    [sg.Frame('',   [[sg.Column(layout_bluearea, background_color=blueArea)]], expand_x=True, expand_y=True, background_color=blueArea, title_location=sg.TITLE_LOCATION_TOP)],
]

window = sg.Window("Simple Annotated Digitization Desk  (SADD)", layout, margins=(2, 2), size=(900,500), resizable=True, finalize=True )
#The three lines below are there to ensure that the cursor in the input text fields is visible. It is invisible against a white background.
window['-NOTES-'].Widget.config(insertbackground='black', highlightcolor='firebrick', highlightthickness=2)
window['-LOGGED-'].Widget.config(insertbackground='black', highlightcolor='firebrick', highlightthickness=2)
window['-DATETIME-'].Widget.config(insertbackground='black', highlightcolor='firebrick', highlightthickness=2)
window['-TAXNAMES-'].Widget.config(insertbackground='black', highlightcolor='firebrick', highlightthickness=2)

def taxonomic_candidates_popup(title, names):
    # This is the window where taxonomic candidate names appear to be selected by the operator
    # title: is the string going into the window bar
    # names: are the taxonomic names submitted by the initial DB query
    names = list(names)
    print(names)
    layout = [
        [sg.Listbox(names, size=(50, 20), font=("Courier New", 16), enable_events=True, key="-LISTBOX-")],
        [sg.StatusBar("", size=(30, 1), key='-STATUS-')],
    ]

    window = sg.Window(title, layout, finalize=True)
    listbox, status = window['-LISTBOX-'], window['-STATUS-']

    while True:

        event, values = window.read()
        if event == sg.WIN_CLOSED or event == 'Exit':
            break
        elif event == '-LISTBOX-':
            selection = values[event]
            if selection:
                item = selection[0]
                index = listbox.get_indexes()[0]
                print(f'Line {index + 1}, {item} selected')
                # break

                window.close()
        elif event == '-EXIT-':
            window.close()

while True:

    event, values = window.read()
    taxon_candidates = None
    #SWITCH CONSTRUCT
    if event == '-STORAGE-':
        print('event:', event)
        print('In storage domain')
    if event == '-PREP-':
        print('In preparation type')
        prepper = values[event]
        print('chosen isss: ', prepper)
    if event == '-TAXON-':
        print('IN taxonomy section')
    if event == '-TYPE-':
        print('IN type status section')
    if event == '-NOTES-':
        print('IN notes section')
    if event == '-TAXNAMES-':
        print('in TAXNAMES -')
        print('len string : ', len(values[event]))

        if len(values[event]) >= 3:
            print('submitted string: ', values[event])
            response = koss.auto_suggest_taxonomy(values[event])
            if response and response[1] <= 20:
                print('the auto suggeter SAYS :) -- ', response[0])
                taxonomic_candidates_popup('Candidate names', response[0])

    if event == sg.WINDOW_CLOSED:
        break

window.close()


""" TO DO:
    Restrict the characters allowed in an input element to digits and . or -
    Accomplished by removing last character input if not a valid character
    This link provides some ideas for input sanitazion https://github.com/PySimpleGUI/PySimpleGUI/issues/1119
"""