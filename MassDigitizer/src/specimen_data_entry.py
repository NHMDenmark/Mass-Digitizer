import PySimpleGUI as sg
import import_csv_memory
import taxonomy_shrinker
""" TO DO:
    Restrict the characters allowed in an input element to digits and . or -
    Accomplished by removing last character input if not a valid character
"""

headlineFont = ("Corbel, 18")
names_ = ['Liliaceae', 'Chloranthales', 'Nymphaeales']
#above should be a complete high level taxonomy that is useful for narrowing the taxon lookup table. Perhaps this is irrelevant as the digitizer will choose 'discipline'
# or taxonomic theme in the log-in part of the app.
preparations = ['pinned', 'alchohol']
geoRegionsCopenhagen = ['Nearctic', 'Palearctic', 'Neotropical', 'Afrotropical', 'Oriental', 'Australian']

headline = [
        sg.Text("Mass Annotated Digitization Desk MADD", font=headlineFont),
        # sg.In(size=(45, 1), enable_events=True, key="-HEADLINE-")
]
hi_taxonomy_prep_type = [sg.Text('Prep Type'), sg.OptionMenu(list(preparations), size=(10,1), key='__PICK_LIST__'), sg.Text('Higher Taxon'),
     sg.OptionMenu(list(names_), size=(10,1), key='__HIGHERTAXON__') ]

barcode_alt_cat = [sg.Text('barcode'), sg.Input(size=(20,1), key='-BARCODE-'), sg.Text('Alt catalog no.'), sg.Input(size=(20,1), key='-ALTCAT-'), sg.Checkbox('Barcode=CatNr', key='-EQUALS-')]
broad_geo_region = [sg.Input(size=(30,1), key='-GEO-')]

layout = [  [headline],
            [hi_taxonomy_prep_type],
            [barcode_alt_cat],
            [sg.Text('BroadGeographical region')],
            [broad_geo_region],
            [sg.Text('Start typing the taxon name')],
            [sg.Input(key='-IN-', size=(30,1), enable_events=True), sg.Checkbox('Type', key='-TYPE-')],
            [sg.Text('Storage')],
            [sg.Input(size=(30, 1), key='-CHOSEN-')],
            [sg.Button('Submit', key='-SUBMIT-')]  ]

window = sg.Window('Mass Digitizer', layout)
taxon_candidates = []
master_dict = {}


def TAX_POPUP(title, names):
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
    if event == '-EXIT-':
        print('exiiiit - - -')
        window.close()
    if event == '-GEO-':
        print('In Geo domain')
    print('event:', event)
    input_string = values[event]
    print('values:', input_string, len(input_string))
    if len(input_string) == 3:
        print('will collect taxonomy based on three char input string!')
        res_dict = import_csv_memory.run_query(input_string)
        print('length of refined taxonomy = ', len(res_dict))
    elif len(input_string) >= 4:
        res_dict = taxonomy_shrinker.refine_taxon_dict(res_dict, input_string)
        print('length of shrunk taxonomy = ', len(res_dict))
        rg = range(1,20)
        if len(res_dict) in rg:
            print('res_dict: ', res_dict)
            ###!
            for key, val in res_dict.items():
                taxon_candidates.append([key, val])
                ###!!
            selected = TAX_POPUP('Candidates', taxon_candidates)

            if selected:

                window['Candidates'].update(selected)
                mask = (taxon_candidates == selected)
                print('selected--:', selected)
                print('[GUI_POPUP] event:', event)
                print('[GUI_POPUP] values:', values)

    if event == sg.WIN_CLOSED or event == 'Bye!':
        break
window.close()
