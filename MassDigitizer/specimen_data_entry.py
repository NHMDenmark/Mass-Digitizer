import PySimpleGUI as sg
import import_csv_memory
import util

lst_higher_taxa = ['Liliaceae', 'Chloranthales', 'Nymphaeales']
lst_preparations = ['pinned', 'alchohol']
lst_geo_regions = ['Nearctic', 'Palearctic', 'Neotropical', 'Afrotropical', 'Oriental', 'Australian']
lst_storage_locations = ['location 1', 'location 2', 'location 3', 'location 4']
lst_type_status = [ 'holotype', 'paratype', 'lectotype', 'no type' ]

sg.theme('Light Grey')

header_font = ("Corbel, 18")
header = [ sg.Text("Mass Annotated Digitisation Desk MADD", font=header_font) ]

ddl_storage_loc = [ sg.Text('Storage Location'), sg.Combo(list(lst_storage_locations), readonly=True, size=(10,1), key='storage') ]
ddl_prep_types = [ sg.Text('Preparation Type'), sg.Combo(list(lst_preparations), readonly=True, size=(10,1), key='preptype') ]
ddl_higher_taxa = [ sg.Text('Taxonomic Group'), sg.Combo(list(lst_higher_taxa), readonly=True, size=(10,1), key='higher_taxon') ]
ddl_type_status = [ sg.Text('Type Status'), sg.Combo(list(lst_type_status), readonly=True, size=(10,1), key='typestatus') ]

txt_barcode_alt_cat = [sg.Text('Barcode'), sg.Input(size=(20,1), key='catalognr'), sg.Text('Alt catalog no.'), sg.Input(size=(20,1), key='-ALTCAT-'), sg.Checkbox('Barcode=CatNr', key='-EQUALS-')]
ddl_broad_geo_region = [
    sg.Text('Broad Geographical region:'), 
    sg.Combo(list(lst_geo_regions), readonly=True, size=(30,1), key='georegion')
    ]

inp_taxonomic_name = [sg.Text('Taxonomic name:'), sg.Input(key='-IN-', size=(30,1), enable_events=True)]

layout = [  [header],
            [
                sg.Column([[sg.Text('box1')]],background_color='#ebf0df', size=(400,200)),
                sg.Column([[sg.Text('box3')]],background_color='lightgrey', size=(300,200))
            ],
            [sg.Column([[sg.Text('box2')]],background_color='#deecf1', size=(400,100))],
            #[sg.Input(size=(30, 1), key='-CHOSEN-')],
            [sg.Button('Save', key='save'), sg.Button('Go back', key='goback')]  
        ]

window = sg.Window('Mass Digitizer', layout, size=(800, 480), background_color='white') #, theme='LightGrey'
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
    print('values:', input_string, len( ))
    if len(input_string) == 3:
        print('will collect taxonomy based on three char input string!')
        res_dict = import_csv_memory.run_query(input_string)
        print('length of refined taxonomy = ', len(res_dict))
    elif len(input_string) >= 4:
        res_dict = util.shrink_dict(res_dict, input_string)
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



""" TO DO:
    Restrict the characters allowed in an input element to digits and . or -
    Accomplished by removing last character input if not a valid character
"""