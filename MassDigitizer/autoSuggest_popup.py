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
- Pop up window for assisting digitizer staff in the data entry effort.
"""


import PySimpleGUI as sg
import data_access as db
from itertools import chain



class AutoSuggest_popup():
    startQueryLimit = 3
    # rowDict = {}
    candidateNamesList = []
    rowCandidates = []

    def __init__(self, table):
        self.tableName = table


    def __exit__(self, exc_type, exc_value, traceback):
        print("\nInside __exit__")

    def auto_suggest(self, name, columnName='name', taxDefItemId=None, rowLimit=200):
        """ Purpose: for helping digitizer staff rapidly input names using return suggestions based on three or
          more entered characters. Function only concerns itself with database lookup.
         name: This parameter is the supplied name from the user.
         rowLimit: at or below this the auto-suggest fires of its names
         returns: a list of names
         TODO implement 'taxonTreeDefid' at convienient time.
        """
        responseType = ''
        # Local variable to determine the auto-suggest type: 'storage', taxon-name, or 'parent taxon-name'.
        # It is included in the return statement.
        cur = db.getDbCursor()

        sql = f"SELECT * FROM {self.tableName} WHERE {columnName} LIKE lower('%{name}%');"

        if taxDefItemId:
            sql = sql[:-1]
            sql = sql + ' AND taxontreedefid = {};'.format(taxDefItemId)

        print('the SQL going into cursor :;;', sql)
        rows = cur.execute(sql).fetchall()

        return rows

    def flatten_rows(self, rowsObject):
        flatCandidates = list(chain.from_iterable(rowsObject))
        rows = list(flatCandidates)
        print('length flattened rows ::: ', len(rows))
        return rows

    def autosuggest_gui(self, partialName, startQuery=3, colName=None):
        # Builds the interface for taxon name lookup as well as for novel names.
        # Parameter partialName is the 'name' as it is being inputted, keystroke-by-keystroke
        # startQuery is an integer on how many key strokes it takes to start the auto-suggester.
        # Can return a novel name if such is inputted.

        choices = [' ']

        input_width = 95
        lines_to_show = 7
        # dimensions of the popup list-box

        layout = [
            [sg.Text('Input Name:', key="lblInputName"),
             sg.Text('Taxon name does not exist. Add higher taxonomy to create new taxon record please.',
                     key='lblNewName', visible=False, background_color='Turquoise3')],
            [sg.Input(size=(input_width, 1), enable_events=True, key='-IN-'),
             sg.Button('', key='btnReturn', visible=False, bind_return_key=True),
             sg.Button('Exit', visible=False)],
            [sg.Text('Input higher taxonomy:', key='lblHiTax', visible=False),
             sg.Input(size=(input_width, 1), enable_events=True, key='txtHiTax', visible=False)],
            # 'btnReturn' is for binding return to nothing in case of a new name and higher taxonomy lacking.
            [sg.pin(
                sg.Col([[sg.Listbox(values=[], size=(input_width, lines_to_show), enable_events=True, key='-BOX-',
                                    bind_return_key=True, select_mode='extended')]],
                       key='-BOX-CONTAINER-', pad=(0, 0), visible=True))], ]

        window = sg.Window('Auto Complete', layout, return_keyboard_events=True, finalize=True, modal=False,
                           font=('Arial', 12), size=(810, 200))
        # The parameter "modal" is explicitly set to False. If True the auto close behavior won't work.

        list_element: sg.Listbox = window.Element(
            '-BOX-')  # store listbox element for easier access and to get to docstrings
        prediction_list, input_text, sel_item = choices, "", 0

        window['-IN-'].update(partialName)
        window.write_event_value('-IN-', partialName)

        while True:  # Event Loop

            window['txtHiTax'].bind('<FocusIn>', '+INPUT FOCUS+')
            event, values = window.read()

            if event is None:
                break

            if event == sg.WIN_CLOSED or event == 'Exit':
                break
            if event is None:
                break

            elif event.startswith('Escape'):
                window['-IN-'].update('')
                window['-BOX-CONTAINER-'].update(visible=False)

            # elif event.startswith('Down') or '16777235' and len(self.candidateNamesList):
            elif event.startswith('Down') and len(self.candidateNamesList):
                sel_item = (sel_item + 1) % len(self.candidateNamesList)
                list_element.update(set_to_index=sel_item, scroll_to_index=sel_item)
            elif event.startswith('Up') and len(self.candidateNamesList):
                sel_item = (sel_item + (len(self.candidateNamesList) - 1)) % len(self.candidateNamesList)
                list_element.update(set_to_index=sel_item, scroll_to_index=sel_item)

            if event.endswith('+TAB'):
                print('pressed TAB')
                break
                window.close()
            ##event IN #####################
            elif event == '-IN-':
                # this concerns all keystrokes except the above ones.
                text = values['-IN-'].lower()

                if text == input_text:
                    continue
                else:
                    input_text = text
                if len(text) >= startQuery:
                    # Kicking off auto-suggest
                    choices = self.auto_suggest(text)
                    candidates = choices

                    self.candidateNamesList = [row['fullname'] for row in candidates]

                    if len(self.candidateNamesList) == 0:
                        # A new name is assumed and user is asked to input it.
                        novelName = sg.popup_get_text('It seems you are entering a name outside the taxonomy.\nPlease check for spelling errors. After finishing the name entry, press OK: ',
                                                      default_text=text)
                        print("The NEW NAME is : ", novelName)
                        return novelName

                    list_element.update(values=self.candidateNamesList, set_to_index=[0])

                sel_item = 0

                ###CALL AUTOsUGGEST_POPUP.py to get the higher taxonomy which is "parentfullname" column

                if len(prediction_list) > 0:
                    print('pred list more than NONE """')
                    window['lblNewName'].update(visible=False)
                    window['lblHiTax'].update(visible=False)
                    window['txtHiTax'].update(visible=False)
                    window['btnReturn'].BindReturnKey = True

                    window['-BOX-CONTAINER-'].update(visible=True)
                else:
                    window['lblInputName'].update('Input higher taxon name:')
                    print('IN taxon input hitax')
                    window['lblNewName'].update(visible=True)
                    print(prediction_list)
                    if len(prediction_list) == 0:
                        window[event].update(value='')
                        prediction_list.append(' ')

            ##event IN #####################

            elif event == 'btnReturn':
                print('pressed Enter/Return || values box= ', values['-BOX-'])

                # Be aware about issues around the popup not being closed properly.
                # Likely to be a PySimpleGUI bug.
                if len(values['-BOX-']) > 0:
                    boxVal = values['-BOX-']
                    if self.tableName == 'storage':
                        column = 'name'
                    else:
                        column = 'fullname'
                    atomicNames = boxVal[0].split('|')
                    atomic = atomicNames.pop()
                    atomic = atomic.strip()
                    print(f"Atomic-{atomic}-", atomic)
                    selected_row = next(row for row in candidates if row[column]==atomic)
                    selected_row = dict(selected_row)
                    print('response to ENTER is;;; ', dict(selected_row))
                    return selected_row

                window.Hide()

        window.Hide()
        window.close()


# EXE section -- remember "taxonname" or "storage"
# ob = AutoSuggest_popup('taxonname')
# ob.autosuggest_gui('')
