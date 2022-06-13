# proto of MADD
#Needs connection to SQLITE3 : https://docs.python.org/3/library/sqlite3.html

import PySimpleGUI as sg


headlineFont = ("Arial, 18")

headline = [

        sg.Text("Mass Annotated Digitization Desk MADD", font=headlineFont),
        # sg.In(size=(45, 1), enable_events=True, key="-HEADLINE-")


]
names_ = ['Pinned', 'Alchohol']
higher_taxon_names = ['Alismatales', 'Pinopsida', 'angiosperms']

# For now will only show the name of the file that was chosen
# image_viewer_column = [
#     [sg.Text("Choose an image from list on left:")],
#     [sg.Text(size=(20, 1), key="-TOUT-")],
#     [sg.Image(key="-IMAGE-")],
# ]

container_Prep_HiTax = [
    [sg.Text('Prep Type'), sg.OptionMenu(list(names_), size=(10,1), key='__PICK_LIST__'), sg.Text('Higher Taxon'),
     sg.OptionMenu(list(higher_taxon_names), size=(10,1), key='__HIGHERTAXON__') ]
]

container_barcode_altcat = [
    [sg.Text("Barcode"), sg.Input(key="__BARCODE__", size=30), sg.Text("Alternative catalog number"), sg.Input(key="__ALTCAT__", size=30)]
]

submit = [
    [sg.FileSaveAs('SUBMIT', initial_folder='/tmp', file_types=(('text files', '*.txt'),))]
]

layout = [
        [headline],
        [sg.Column(container_Prep_HiTax)],       # sg.VSeperator(),
        [sg.Column(container_barcode_altcat)],
        [sg.Column(submit)]
        ]


window = sg.Window("Image Viewer", layout)

while True:
    event, values = window.read()
    if event == "Exit" or event == sg.WIN_CLOSED:
        break