import PySimpleGUI as sg
import data_access as db
from itertools import chain
# import additional_popup
import tkinter as tk
import itertools


class AutoSuggest_popup():
    startQueryLimit = 3
    # rowDict = {}
    candidateNamesList = []
    rowCandidates = []

    def __init__(self, table):
        # self.startQuery = startQueryLimit
        self.tableName = table


    def __exit__(self, exc_type, exc_value, traceback):
        print("\nInside __exit__")

    # def responsePacker(self, nameList):
    #     # if candidateType == 'storage':
    #     print("CANDIDATES len | ", len(nameList))
    #     # nm = choices[0][0][2]
    #     header = nameList.keys()
    #     storageName = header[2]
    #     print(storageName)
    #
    #     for row in nameList:
    #         print("row @ name ;;", len(row), row['name'])
    #         particularRow = dict(row)
    #         self.rowDict[row['name']] = particularRow
    #         # print(dict(row[0]))
    #     self.candidateNamesList = list(self.rowDict.keys())
    #     print("rowDict.keys())", self.rowDict.keys())
    #     print("candidateNamesList - - - ", self.candidateNamesList[-5:])
    #     # print("row shelf 7 :;:; ", rowDict['Shelf 7'])
    #     print('FIRST row = ', dict(itertools.islice(self.rowDict.items(), 3)))
    #     return self.candidateNamesList

    def auto_suggest(self, name, columnName='name', taxDefItemId=None, rowLimit=200):
        """ Purpose: for helping digitizer staff rapidly input names by returning suggestions based on the three or
          more entered characters. Function only concerns itself with database lookup.
         name: This parameter is the supplied name from the user.
         rowLimit: at or below this the auto-suggest fires of its names
         returns: a list of names
         TODO implement 'taxonTreeDefid' at convienient time.
        """
        responseType = ''
        # Local variable to determine the auto-suggest type: 'storage', taxon-name, or 'parent taxon-name'.
        # It is included in the return statement.
        print('ååååååå IN auto /// supplied partial name is ::', name)
        cur = db.getDbCursor()
        # if self.tableName == 'taxonname' and columnName == 'fullname':
        print(f'query on {self.tableName}')
        sql = f"SELECT * FROM {self.tableName} WHERE {columnName} LIKE lower('{name}%');"

        if taxDefItemId:
            sql = sql[:-1]
            sql = sql + ' AND taxontreedefid = {};'.format(taxDefItemId)
            print(sql)
        print('the SQL going into cursor :;;', sql)
        rows = cur.execute(sql).fetchall()

        print('&&\n len rows = ', len(rows), '\n¤¤¤')
        # rows[0][0][2]
        if len(rows) < 20:
            for j in rows:
                print(j)
        # if lengthOfRows <= rowLimit:

        return rows, responseType

    def flatten_rows(self, rowsObject):
        flatCandidates = list(chain.from_iterable(rowsObject))
        rows = list(flatCandidates)
        print('length flattened rows ::: ', len(rows))
        return rows

    def autosuggest_gui(self, partialName, startQuery=3, colName=None):
        # Builds the interface for taxon name lookup as well as for novel names.
        # Parameter partialName is the 'name' as it is being inputted, keystroke-by-keystroke
        # startQuery is an integer on how many key strokes it takes to start the auto-suggester.

        choices = [' ']

        if colName:
            print('colName == ', colName)
            choices = self.auto_suggest(self.tableName, partialName, columnName=colName)
            print('IN the tablename that is ;:', choices[1])
            # choices_list = self.flatten_rows(choices[0])
        elif colName == 'storage':
            print('! !STORAGE function ...')
            choices = self.auto_suggest(partialName)

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
        # cREATE A dict with name as key and the record as value
        # header = choices[0].keys()
        # pList =

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
                print('EVENT  , NONE')
                break
            # pressing down arrow will trigger event -IN- then aftewards event Down:40
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
                res = ''

                if text == input_text:
                    continue
                else:
                    input_text = text
                if len(text) >= startQuery:
                    choices = self.auto_suggest(text)
                    print('len(choices) & type ::: ', len(choices[0]), type(choices[0]))
                    candidates = choices[0]
                    print('####&&&&&&&&&&&&&', [dict(row) for row in candidates])
                    print('auto trigger - - "text" longer than 3..& type choices == ', type(candidates))
                    self.candidateNamesList = [row['fullname'] for row in candidates]
                    print("pressed recs -- -- ", self.candidateNamesList)

                    list_element.update(values=self.candidateNamesList, set_to_index=[0])


                    # acquire row belonging to the name

                sel_item = 0
                # list_element.update(set_to_index=sel_item)

                ###CALL AUTOsUGGEST_POPUP.py to get the higher taxonomy which is "parentfullname" column

                # if len()
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
                    textInput = values[event]

            ##event IN #####################

            elif event == 'btnReturn':
                print('pressed Enter/Return || values box= ', values['-BOX-'])
                # window.Hide()
                # A patch on the issue around the popup not being closed properly.
                # Likely to be a PySimpleGUI bug.
                if len(values['-BOX-']) > 0:
                    boxVal = values['-BOX-']

                    response = boxVal[0]
                    print('response to ENTER is;;; ', response)
                    return response

                window.Hide()

        window.Hide()
        window.close()


# EXE section -- remember "taxonname" or "storage"
# ob = AutoSuggest_popup('taxonname')
# ob.autosuggest_gui('')
