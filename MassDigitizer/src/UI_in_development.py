import PySimpleGUI as sg

def check_frame():
    return sg.Frame("Multispecimen sheet:", [[sg.Checkbox('')]], pad=(5, 3), expand_x=True, expand_y=False, background_color='#d3ffce', border_width=0)

sg.theme('Material2')
blueArea = '#99ccff'
greenArea = '#ccffcc'
greyArea = '#e6e6e6'

institutions = ['NHMD: Natural History Museum of Denmark (Copenhagen)', 'NHMA: Natural History Museum Aarhus', 'TEST: Test server']
prepType = ['pinned', 'herbarium sheets']
taxonomicGroups = ['placeholder...']
typeStatus =  ['placeholder...']
#Georegions -v
geoRegionsCopenhagen = ['Nearctic', 'Palearctic', 'Neotropical', 'Afrotropical', 'Oriental', 'Australian']
taxonomicNames = ['Acanthohelicospora aurea','Acremonium alternatum','Actinonema actaeae','Aegerita alba','Agaricus aestivalis','Agaricus aestivalis var. flavotacta','Agaricus altipes']
barcode = [58697014]
collections = ['Botany', 'Entomology', 'Ichthyology']
workstations = ['Commodore_64', 'VIC_20', 'HAL2000', 'Cray']

defaultSize = (20,1)

storage = [
                    sg.Text("Storage location:", size=defaultSize, background_color=greenArea),
                    sg.Combo(institutions, key='-STORAGE-', text_color='black', background_color='white'),
                ]

preparation = [
                    sg.Text("Preparation type:", size=defaultSize, background_color=greenArea),
                    sg.Combo(prepType, key='-PREP-',text_color='black', background_color='white'),
                    ]

taxonomy = [
                    sg.Text("Taxonomic group:", size=defaultSize, background_color=greenArea),
                    sg.Combo(taxonomicGroups, key='-TAXON-',text_color='black', background_color='white'),
                    ]

type_status = [
                    sg.Text('Type status:', size=defaultSize, background_color=greenArea),
                    sg.Combo(typeStatus, key='-TYPE-', text_color='black', background_color='white'),
                 ]

notes = [sg.Text('Notes', size=defaultSize, background_color=greenArea), sg.InputText(size=(24,1), background_color='white', text_color='black', key='-NOTES-'),
         ]

layout_frame1 = [
    # [sg.Frame('Multispecimen', [sg.Checkbox('My Checkbox', default=True)],)],
    storage, preparation, taxonomy, type_status, notes, [sg.Checkbox('Multispecimen sheet', background_color=greenArea)],
    # [sg.Frame("Multispecimen sheet", [[check_frame()]], pad=(5, 3), expand_x=True, expand_y=True, size=(280, 40), title_location=sg.TITLE_LOCATION_TOP)],

]

broadGeo = [
                    sg.Text('Broad geographic region:', size=defaultSize ,background_color=blueArea, text_color='black'),
                    sg.Combo(geoRegionsCopenhagen, key='-GEOREGION-', text_color='black', background_color='white'),
                 ]

taxonomicName = [
                    sg.Text('Taxonomic name:', size=defaultSize, background_color=blueArea, text_color='black'),
                    sg.Combo(taxonomicNames, key='-TAXNAMES-', text_color='black', background_color='white'),
                 ]

barcode = [
                    sg.Text('Barcode:', size=defaultSize, background_color=blueArea, text_color='black'),
                    sg.Combo(barcode, key='-BARCODE-', text_color='black', background_color='white'),
                 ]

layout_frame22 = [
    broadGeo, taxonomicName, barcode,
    [sg.Button('SAVE', key="-SAVE-", button_color='seagreen'), sg.Button('Go Back', key="-GOBACK-", button_color='firebrick', pad=(120,0))]
]

loggedIn = [sg.Text('Logged in as:', size=defaultSize, background_color=greyArea), sg.InputText(size=(24,1), background_color='white', text_color='black', key='-LOGGED-'),
         ]

dateTime = [sg.Text('Date / Time:', size=defaultSize, background_color=greyArea), sg.InputText(size=(24,1), background_color='white', text_color='black', key='-DATETIME-'),
         ]

institution_ = [sg.Text('Institution:', size=defaultSize, background_color=greyArea), sg.Combo(institutions, key="-INSTITUTION-", text_color='black', background_color='white'),
         ]

collections =  [sg.Text('Collection name:', size=defaultSize, background_color=greyArea), sg.Combo(collections, key="-COLLECTION-", text_color='black', background_color='white'),
         ]

work_station =  [sg.Text('Workstation:', size=defaultSize, background_color=greyArea), sg.Combo(workstations, key="-WORKSTATION-", text_color='black', background_color='white'),
         ]

settings_ = [sg.Text('Settings ', size=defaultSize, justification='center', background_color=greyArea), sg.Button('', image_filename=r'options_gear.png',
                                                                                          button_color=greyArea, key='-SETTING-', border_width=0)
         ]

layout_grey = [loggedIn, dateTime, [sg.Text("_______________" * 5, background_color=greyArea)], institution_,
               collections, work_station, settings_, [sg.Button('LOG OUT', key="-LOGOUT-", button_color='grey40')]]

layout = [
    [sg.Frame('green area',  [[sg.Column(layout_frame1, background_color=greenArea)]], size=(250,200), expand_x=True, expand_y=True, background_color=greenArea),
     sg.Frame('grey area',   [[sg.Column(layout_grey, background_color=greyArea)]], size=(250,300), expand_x=True, expand_y=True, background_color=greyArea)],
    [sg.Frame('blue area',   [[sg.Column(layout_frame22, background_color=blueArea)]], expand_x=True, expand_y=True, background_color=blueArea, title_location=sg.TITLE_LOCATION_TOP)],
]

window = sg.Window("Simple Annotated Digitization Desk  (SADD)", layout, margins=(2, 2), size=(900,500), resizable=True, finalize=True, )
window['-NOTES-'].Widget.config(insertbackground='black', highlightcolor='firebrick', highlightthickness=2)
window['-LOGGED-'].Widget.config(insertbackground='black', highlightcolor='firebrick', highlightthickness=2)
window['-DATETIME-'].Widget.config(insertbackground='black', highlightcolor='firebrick', highlightthickness=2)

while True:

    event, values = window.read()
    if event == sg.WINDOW_CLOSED:
        break

window.close()