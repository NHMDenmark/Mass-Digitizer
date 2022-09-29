# -*- coding: utf-8 -*-
"""
Created on August 26 2022

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
import data_access as db
from itertools import chain

def taxonomic_autosuggest_gui(partialName):
    # TODO Function contract 
    # The list of choices that are going to be searched
    # In this example, the PySimpleGUI Element names are used
    choices = auto_suggest_taxonomy(partialName)
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

    window = sg.Window('AutoComplete', layout, return_keyboard_events=True, finalize=True, modal=False,
                       font=('Helvetica', 16))
    # The parameter "modal" is explicitly set to False. If True the auto close behavior
    # won't work.

    list_element: sg.Listbox = window.Element('-BOX-')  # store listbox element for easier access and to get to docstrings
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

def small_list_lookup(tableName, inputKey, indicesForColumn=2):
    ###For retreiving values stored in the minor tables ('institution' and 'collection')
    #tableName: String can be 'Storage location', ' Prep type' , 'institution', etc.
    #inputKey: Is the field key from the specimen_data_entry interface like: Prep type, Broad geographic region

    #return: content of particular table

    rows = db.getRows(tableName, limit=200)

    result = rows
    return result


def auto_suggest_taxonomy(name, taxDefItemId=None, rowLimit=200):
    # Purpose: for helping digitizer staff rapidly input names by returning suggestions based on the three or
    #  more entered characters.
    #trigger: means how many keystrokes it takes to trigger the auto-suggest functionality
    #rowLimit: at or below this the auto-suggest fires of its names
    #returns: a list of names

    cur = db.getDbCursor()
    sql = "SELECT fullname FROM taxonname WHERE fullname LIKE lower('% {}%') " \
          "OR fullname LIKE lower('{}%');".format(name, name)
    print('In autosuggest & sql isz: ', sql)
    if taxDefItemId:
        sql = sql[:-1]
        sql = sql + ' AND taxontreedefid = {};'.format(taxDefItemId)
        print(sql)
    rows = cur.execute(sql).fetchall()

    print('len rows = ', len(rows))
    lengthOfRows =len(rows)
    #if lengthOfRows <= rowLimit:
    print('AUTOSUGGEST!!!')
    flatCandidates = list(chain.from_iterable(rows))
    # print(flatCandidates)
    rows = list(flatCandidates)
    
    return rows
