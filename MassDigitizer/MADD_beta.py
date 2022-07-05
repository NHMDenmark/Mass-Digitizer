import PySimpleGUI as sg
import import_csv_memory
import taxonomy_shrinker
"""
    Restrict the characters allowed in an input element to digits and . or -
    Accomplished by removing last character input if not a valid character
"""

headlineFont = ("Corbel, 18")
names_ = ['Liliaceae', 'Chloranthales', 'Nymphaeales']
preparations = ['pinned', 'alchohol']

headline = [
        sg.Text("Mass Annotated Digitization Desk MADD", font=headlineFont),
        # sg.In(size=(45, 1), enable_events=True, key="-HEADLINE-")
]
hi_taxonomy_prep_type = [sg.Text('Prep Type'), sg.OptionMenu(list(preparations), size=(10,1), key='__PICK_LIST__'), sg.Text('Higher Taxon'),
     sg.OptionMenu(list(names_), size=(10,1), key='__HIGHERTAXON__') ]

layout = [  [headline],
            [hi_taxonomy_prep_type],
            [sg.Text('Start typing the taxon name')],
            [sg.Input(key='-IN-', enable_events=True)],
            [sg.Text('Taxonomic candidates', size=(20, 1)), sg.Input(size=(20, 1), key='-NAMELIST-'), sg.Button('SELECTION')],
            [sg.Button('Exit')]  ]

window = sg.Window('Floating point input validation', layout)
taxon_candidates = None


def GUI_POPUP(title, names):
    names = list(names)
    print(names)
    layout = [
        [sg.Listbox(names, size=(30, 5), font=("Courier New", 16), enable_events=True, key="-LISTBOX-")],
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
                print(f'Line {index + 1}, "{item}" selected')
                break

    window.close()

    # if values and values['-SELECTED-']:
    #     return values['-SELECTED-']

while True:
    event, values = window.read()
    print('event:', event)
    input_string = values[event]
    print('values:', input_string, len(input_string))
    if len(input_string) == 3:
        print('off to ICM we go!')
        res_dict = import_csv_memory.run_query(input_string)
        print('length of refined taxonomy = ', len(res_dict))
    elif len(input_string) >= 4:
        res_dict = taxonomy_shrinker.refine_taxon_dict(res_dict, input_string)
        print('length of shrunk taxonomy = ', len(res_dict))
        if len(res_dict) < 20:
            print(res_dict)
            taxon_candidates = res_dict.keys()
            selected = GUI_POPUP('Candidates', taxon_candidates)

            if selected:
                # window['Candidates'].update(selected[0])
                window['Candidates'].update(selected)
                mask = (taxon_candidates == selected)
                print('selected--:', selected)
                print('[GUI_POPUP] event:', event)
                print('[GUI_POPUP] values:', values)

    if event == sg.WIN_CLOSED or event == 'Bye!':
        break
window.close()