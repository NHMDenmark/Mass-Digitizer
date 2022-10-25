import PySimpleGUI as sg
import data_access as db
from itertools import chain
# import additional_popup
import tkinter as tk

class AutoSuggest_popup():

    startQueryLimit = 3
    
    def __init__(self, table):
        # self.startQuery = startQueryLimit
        self.tableName = table
        self.popped = False

    def __exit__(self, exc_type, exc_value, traceback):
        print("\nInside __exit__")

    def auto_suggest(self, tableName, name, columnName='fullname', taxDefItemId=None, rowLimit=200):
        # Purpose: for helping digitizer staff rapidly input names by returning suggestions based on the three or
        #  more entered characters.
        # trigger: means how many keystrokes it takes to trigger the auto-suggest functionality
        # rowLimit: at or below this the auto-suggest fires of its names
        # returns: a list of names
        # TODO implement 'taxonTreeDefid' at convienient time.
        cur = db.getDbCursor()
        if self.tableName == 'taxonname':
            sql = f"SELECT fullname FROM {tableName} WHERE {columnName} LIKE lower('% {name}%') OR {columnName} LIKE lower('{name}%');"
        else:
            sql =f"SELECT fullname FROM storage WHERE name LIKE '{name}%'"
        
        if taxDefItemId:
            sql = sql[:-1]
            sql = sql + ' AND taxontreedefid = {};'.format(taxDefItemId)
            print(sql)
        rows = cur.execute(sql).fetchall()

        print('len rows = ', len(rows))
        # if lengthOfRows <= rowLimit:
        flatCandidates = list(chain.from_iterable(rows))
        rows = list(flatCandidates)
        print('length flattened rows ::: ', len(rows))

        return rows

    def autosuggest_gui(self, partialName, startQuery=3, colName=None):
        # TODO Function contract
        # Parameter partialName is the 'name' as it is being inputted, keystroke-by-keystroke
        # startQuery is an integer on how many key strokes it takes to start the auto-suggester.
        print('IN autosuggest_GUI :.: ', partialName, self.tableName)
        if colName:
            print('colName == ', colName)
            choices = self.auto_suggest(self.tableName, partialName, columnName=colName)
        else:
            print('No set colname! Normal function ...')
            choices = self.auto_suggest(self.tableName, partialName)
        print(type(choices))

        input_width = 95
        lines_to_show = 5
        # dimensions of the popup box

        layout = [
            [sg.Text('Input Name:'), sg.Text('Taxon not found. Please add higher taxonomy to create new taxon record?', key='lblNewName', visible=False, background_color='Turquoise3')],
            [sg.Input(size=(input_width, 1), enable_events=True, key='-IN-'),
             sg.Button('', key='btnReturn', visible=False, bind_return_key=True),
             sg.Button('Exit', visible=False)],
            [sg.Text('Input higher taxonomy:', key='lblHiTax', visible=False), sg.Input(size=(input_width, 1), enable_events=True, key='txtHiTax', visible=False)],
            # 'btnReturn' is for binding return to nothing in case of a new name and higher taxonomy lacking.
            [sg.pin(
                sg.Col([[sg.Listbox(values=[], size=(input_width, lines_to_show), enable_events=True, key='-BOX-', select_mode=sg.LISTBOX_SELECT_MODE_SINGLE)]],
                       key='-BOX-CONTAINER-', pad=(0, 0), visible=True))],]

        window = sg.Window('Auto Complete', layout, return_keyboard_events=True, finalize=True, modal=False,
                           font=('Arial', 12), size=(810,200))
        # The parameter "modal" is explicitly set to False. If True the auto close behavior won't work.

        list_element: sg.Listbox = window.Element('-BOX-')  # store listbox element for easier access and to get to docstrings
        prediction_list, input_text, sel_item = choices, "", 0
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
            elif event.startswith('Down') and len(prediction_list):
                sel_item = (sel_item + 1) % len(prediction_list)
                list_element.update(set_to_index=sel_item, scroll_to_index=sel_item)
            elif event.startswith('Up') and len(prediction_list):
                sel_item = (sel_item + (len(prediction_list) - 1)) % len(prediction_list)
                list_element.update(set_to_index=sel_item, scroll_to_index=sel_item)


            if event.endswith('+TAB'):
                print('pressed TAB')
                break
                window.close()

            elif event == '-IN-':
                # this concerns all keystrokes except the above ones.
                text = values['-IN-'].lower()

                if text == input_text:
                    continue
                else:
                    input_text = text
                if len(text) < len(partialName):
                    choices = self.auto_suggest(self.tableName, text)
                    print('in line 110 - 112')
                prediction_list = []
                print('pressed key', values['-IN-'])
                if len(text) >= len(partialName):
                    # condition for activating the autosuggest feature.
                    prediction_list = [item for item in choices if item.lower().find(text) != -1]

                list_element.update(values=prediction_list)
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
                    window['-BOX-CONTAINER-'].update(visible=False)

            elif event == 'txtHiTax':
                # window.bind("<KeyPress>", "kPress")
                print('1n hiTAX')
            elif event == '-BOX-':
                window['-IN-'].update(value=values['-BOX-'])
                window['-BOX-CONTAINER-'].update(visible=False)

            elif event == 'btnReturn':
                print('pressed Enter/Return || len values box= ', len(values['-BOX-']))
                # window.Hide()
                # A patch on the issue around the popup not being closed properly.
                # Likely to be a PySimpleGUI bug.
                if len(values['-BOX-']) > 0:
                    boxVal = values['-BOX-']

                    #sql = "SELECT id, name, fullname FROM {} WHERE fullname = '{}'".format(self.tableName, boxVal[0])
                    #print(sql)
                    #boxID = db.executeSqlStatement(sql)

                    #print([item for item in boxID])
                    #print('Selected boxvalue is -/ '
                    #      , boxVal[0])
                    #return boxVal[0]

                    records = db.getRowsOnFilters(f'{self.tableName}',{'fullname': f'="{boxVal[0]}"'})
                    
                    if len(records)==1:
                        return records[0]
                    else: 
                        return None
                window.Hide()
            #         window['-IN-'].update(value=boxVal[0])
            # event is None
                # window['-BOX-CONTAINER-'].update(visible=False)
                # tk.Tk.protocol("WM_DELETE_WINDOW", on_closing)


                    # window.Hide()
        
        window.Hide()
        window.close()
# EXE section -- remember "taxonname"
# ob = AutoSuggest_popup('storagreturn
