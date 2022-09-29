import PySimpleGUI as sg
import data_access as db
from itertools import chain


class AutoSuggest_popup():
    def __init__(self, table):
        self.tableName = table

    def auto_suggest_taxonomy(self, tableName, name, taxDefItemId=None, rowLimit=200):
        # Purpose: for helping digitizer staff rapidly input names by returning suggestions based on the three or
        #  more entered characters.
        # trigger: means how many keystrokes it takes to trigger the auto-suggest functionality
        # rowLimit: at or below this the auto-suggest fires of its names
        # returns: a list of names
        # TODO implement 'taxonTreeDefid' at convienient time.
        cur = db.getDbCursor()
        if self.tableName == 'taxonname':
            sql = f"SELECT fullname FROM {tableName} WHERE fullname LIKE lower('% {name}%') OR fullname LIKE lower('{name}%');"

        else:
            sql =f"SELECT fullname FROM storage WHERE name LIKE '{name}%'"
        print('In autosuggest & sql isz: ', sql)
        if taxDefItemId:
            sql = sql[:-1]
            sql = sql + ' AND taxontreedefid = {};'.format(taxDefItemId)
            print(sql)
        rows = cur.execute(sql).fetchall()

        print('len rows = ', len(rows))
        # if lengthOfRows <= rowLimit:
        flatCandidates = list(chain.from_iterable(rows))
        rows = list(flatCandidates)

        return rows

    def autosuggest_gui(self, partialName):
        # TODO Function contract
        # Parameter partialName is the 'name' as it is being inputted, keystroke-by-keystroke
        # The list of choices that are going to be searched
        # In this example, the PySimpleGUI Element names are used
        choices = self.auto_suggest_taxonomy(self.tableName, partialName)
        print(type(choices))

        print('len of choices is; ', len(choices), type(choices), '\n choices are;; ', choices)
        # sorted([elem.__name__ for elem in sg.Element.__subclasses__()])

        input_width = 95
        lines_to_show = 5
        # dimensions of the popup box

        layout = [
            [sg.Text('Input Name:')],
            [sg.Input(size=(input_width, 1), enable_events=True, key='-IN-')],
            [sg.pin(
                sg.Col([[sg.Listbox(values=[], size=(input_width, lines_to_show), enable_events=True, key='-BOX-', select_mode=sg.LISTBOX_SELECT_MODE_SINGLE)]],
                       key='-BOX-CONTAINER-', pad=(0, 0), visible=True))],]

        window = sg.Window('AutoComplete', layout, return_keyboard_events=True, finalize=True, modal=False,
                           font=('Arial', 12), size=(810,200))
        # The parameter "modal" is explicitly set to False. If True the auto close behavior
        # won't work.

        list_element: sg.Listbox = window.Element('-BOX-')  # store listbox element for easier access and to get to docstrings
        prediction_list, input_text, sel_item = choices, "", 0
        window['-IN-'].update(partialName)
        window.write_event_value('-IN-', partialName)
        # global windowAutosuggest
        # windowAutosuggest = window

        while True:  # Event Loop

            event, values = window.read()
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
                    print('Selected boxval ISS - ', boxVal[0])
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

r = AutoSuggest_popup('taxonname')
r.autosuggest_gui('delta')