import PySimpleGUI as sg
import data_access as db
from itertools import chain
# import additional_popup
import tkinter as tk
import itertools

class AutoSuggest_popup():

    startQueryLimit = 3
    lfList = []

    def __init__(self, table):
        # self.startQuery = startQueryLimit
        self.tableName = table
        self.popped = False
        self.candidateNamesList = []

    def __exit__(self, exc_type, exc_value, traceback):
        print("\nInside __exit__")

    def auto_suggest(self, tableName, name, columnName='fullname', taxDefItemId=None, rowLimit=200):
        """ Purpose: for helping digitizer staff rapidly input names by returning suggestions based on the three or
          more entered characters. Function only concerns itself with database lookup.
         rowLimit: at or below this the auto-suggest fires of its names
         returns: a list of names
         TODO implement 'taxonTreeDefid' at convienient time.
        """
        responseType = ''

        cur = db.getDbCursor()
        if self.tableName == 'taxonname' and columnName == 'fullname':
            print('just taxon name')
            sql = f"SELECT * FROM {tableName} WHERE {columnName} LIKE lower('% {name}%') OR {columnName} LIKE lower('{name}%');"

        elif self.tableName == 'taxonname' and columnName == 'parentfullname':
            print("INNN PPPPPARRRRRRRRENTT")
            sql = f"SELECT DISTINCT {columnName} AS parentfullname FROM {tableName} WHERE {columnName} LIKE lower('{name}%')"
            print('--------------',sql,'----')
            responseType = 'taxon'
        else:
            sql =f"SELECT * FROM storage WHERE name LIKE '{name}%'"
            responseType = 'storage'
        
        if taxDefItemId:
            sql = sql[:-1]
            sql = sql + ' AND taxontreedefid = {};'.format(taxDefItemId)
            print(sql)
        rows = cur.execute(sql).fetchall() , tableName

        # print('len rows = ', len(rows))
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
        print('IN autosuggest_GUI :.: ', partialName, self.tableName)
        choices = [' ']
        choices_list = []
        if colName:
            print('colName == ', colName)
            choices = self.auto_suggest(self.tableName, partialName, columnName=colName)
            print('IN the tablename that is ;:', choices[1])
            choices_list = self.flatten_rows(choices[0])
        elif colName == 'storage':
            print('! !STORAGE function ...')
            choices = self.auto_suggest(self.tableName, partialName)
        print(type(choices))

        input_width = 95
        lines_to_show = 5
        # dimensions of the popup box

        layout = [
            [sg.Text('Input Name:', key="lblInputName"), sg.Text('Taxon name does not exist. Add higher taxonomy to create new taxon record please.', key='lblNewName', visible=False, background_color='Turquoise3')],
            [sg.Input(size=(input_width, 1), enable_events=True, key='-IN-'),
             sg.Button('', key='btnReturn', visible=False, bind_return_key=True),
             sg.Button('Exit', visible=False)],
            [sg.Text('Input higher taxonomy:', key='lblHiTax', visible=False), sg.Input(size=(input_width, 1), enable_events=True, key='txtHiTax', visible=False)],
            # 'btnReturn' is for binding return to nothing in case of a new name and higher taxonomy lacking.
            [sg.pin(
                sg.Col([[sg.Listbox(values=[], size=(input_width, lines_to_show), enable_events=True, key='-BOX-', bind_return_key=True, select_mode=sg.LISTBOX_SELECT_MODE_SINGLE)]],
                       key='-BOX-CONTAINER-', pad=(0, 0), visible=True))],]

        window = sg.Window('Auto Complete', layout, return_keyboard_events=True, finalize=True, modal=False,
                           font=('Arial', 12), size=(810,200))
        # The parameter "modal" is explicitly set to False. If True the auto close behavior won't work.

        list_element: sg.Listbox = window.Element('-BOX-')  # store listbox element for easier access and to get to docstrings
        prediction_list, input_text, sel_item = choices, "", 0
        #cREATE A dict with name as key and the record as value
        # header = choices[0].keys()
        # pList =
        print("choices øøøøø : ",choices, len(choices))
        window['-IN-'].update(partialName)
        window.write_event_value('-IN-', partialName)

        while True:  # Event Loop

            window['txtHiTax'].bind('<FocusIn>', '+INPUT FOCUS+')
            event, values = window.read()

            if event is None:
                break
            # window.bind('<Key>', 'keyPress')
            operational_name = values['-IN-']
            if event == sg.WIN_CLOSED or event == 'Exit':
                break
            if event is None:
                print('EVENT  , NONE')
                break
            # pressing down arrow will trigger event -IN- then aftewards event Down:40
            elif event.startswith('Escape'):
                window['-IN-'].update('')
                window['-BOX-CONTAINER-'].update(visible=False)

            elif event.startswith('Down') or '16777235' and len(self.candidateNamesList):
                print('pressed down &', len(self.candidateNamesList))
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
                if len(text) >= 3:
                    choices = self.auto_suggest(self.tableName, text)
                    # print('len(choices) & type ::: ', choices[1], len(choices[0][0]), choices)
                    candidates = choices[0][0]
                    candidateType = choices[1]
                    print(f"the candidate type is: {candidateType}")
                    print('in line 110 - 112')
                    print('auto trigger - - "text" longer than 3..& type choices == ', type(choices))
                    #Test to see if choices is row or list
                    if candidateType == 'storage':
                        print("CANDIDATES len | ", len(candidates))
                        # nm = choices[0][0][2]
                        header = candidates[0].keys()
                        storageName = header[2]
                        print(storageName)
                        rowDict = {}
                        for row in candidates:
                            # print("row @ name ;;", len(row), row['name'])
                            particularRow = dict(row)
                            rowDict[row['name']] = particularRow
                            # print(dict(row[0]))
                        self.candidateNamesList = list(rowDict.keys())
                        print("rowDict.keys())", rowDict.keys())
                        # print("row shelf 7 :;:; ", rowDict['Shelf 7'])
                        print('FIRST row = ', dict(itertools.islice(rowDict.items(), 3)))
                        for row in choices[0]:
                            prediction_list.append(row[2])
                        # prediction_list = [item[2] for item[2] in choices[0] if item.lower().find(text) != -1]
                        prediction_list.pop(0)
                        print('sample of candidate names list::: ', self.candidateNamesList)
                    else:
                        print('choices is NOT a list||! but ', type(choices[0]))

                print('pressed key;', values['-IN-'])
                # if len(text) >= len(partialName):
                    # condition for activating the autosuggest feature.
                print('auto trigger - - "text" longer than partial name..\n',type(self.candidateNamesList), self.candidateNamesList[0:4])
                print("input text ------------ ", text, input_text)
                candidate_list = [item for item in self.candidateNamesList if item.find(text) != -1]
                print('camdidate lust: ', self.candidateNamesList)

                list_element.update(values=self.candidateNamesList)
                sel_item = 0
                list_element.update(set_to_index=sel_item)
                # if len(prediction_list) == 0:
                #     print('Prediction list == 0,,, potential new name!? ')
                #     window.set_title("Higher taxon autosuggest")
                #     window['lblNewName'].update(visible=True)
                #     window['btnReturn'].BindReturnKey = False
                #     window['lblHiTax'].update(visible=True)
                #     window['txtHiTax'].update(visible=True)
                #     window.bind("<KeyPress>", "kPress")
                #     if event in ("kPress"):
                #         print('key pressed : ', values['txtHiTax'])
                #     hiTax = window['txtHiTax'].get()
                #     print('press / event is ; ', event, hiTax)
                #     if len(hiTax) >= 3:
                #         print('HiTax is -- ', window['txtHiTax'].get())
                #         resHT = additional_popup.highTaxLookup(window['txtHiTax'])
                #         rowsHT = self.autosuggest_gui(hiTax, colName='parentfullname')
                #         print("highher taxonomy candidates arr: : ", rowsHT)
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
                        window[event].update(value ='')
                        prediction_list.append(' ')
                    textInput = values[event]

##event IN #####################
                    # prediction_list.append(textInput)
                    # window['-IN-'].update(background_color='red') DISABLE below resets the background color - sorry
                    # window['-IN-'].update(disabled=True)
                    # window['lblHiTax'].update(visible=True)
                    # window['txtHiTax'].update(visible=True)
                    # window['txtHiTax'].set_focus()

            # elif event == 'txtHiTax':
            #     # window['btnReturn'].BindReturnKey = True
            #     textInput = values[event]
            #     if len(textInput) >= 3:
            #         choices = self.auto_suggest('taxonname', textInput, columnName='parentfullname')
            #         # res = self.auto_suggest('taxonname', textInput, columnName='parentfullname')
            #         print('In txtHiTax and candidate list length is:: ', len(choices))
            #         prediction_list = []
            #
            #         if len(choices) <= 200:
            #             window['btnReturn'].BindReturnKey = True
            #             print("INNNNNNNNNNNNNN under 200 !!!")
            #             # condition for activating the autosuggest feature.
            #
            #             prediction_list = [item for item in choices if item.lower().find(text) != -1]
            #             sel_item = 0
            #             list_element.update(set_to_index=sel_item)
            #             # list_element.update(values=prediction_list, visible=True)
            #             window['-BOX-'].update(values=choices, visible=True)
            #     print(values[event])
            # elif event == '-BOX-':
            #     window['-IN-'].update(value=values['-BOX-'])
            #     window['-BOX-CONTAINER-'].update(visible=False)

            elif event == 'btnReturn':
                print('pressed Enter/Return || len values box= ', len(values['-BOX-']))
                # window.Hide()
                # A patch on the issue around the popup not being closed properly.
                # Likely to be a PySimpleGUI bug.
                if len(values['-BOX-']) > 0:
                    boxVal = values['-BOX-']

                    response = boxVal[0]
                    currentRecord = rowDict[response]
                    print('===============Selected boxvalue is -/- ', response)
                    print('rrrrrrrrrrrrrrrrrretrurned record  ', currentRecord)
                    return response, currentRecord

                    # records = db.getRowsOnFilters(f'{self.tableName}',{'fullname': f'="{boxVal[0]}"'})
                    #
                    # if len(records)==1:
                    #
                    #     return records[0]
                    # else:
                    #     return None
                window.Hide()
        
        window.Hide()
        window.close()
# EXE section -- remember "taxonname"
ob = AutoSuggest_popup('storage')
ob.autosuggest_gui('')
