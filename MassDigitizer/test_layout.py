import PySimpleGUI as sg

# internal dependencies
import util
import data_access as db
import global_settings as gs
# import home_screen as hs
import kick_off_sql_searches as koss

# Make sure that current folder is registrered to be able to access other app files
# sys.path.append(str(pathlib.Path(__file__).parent.parent.joinpath('MassDigitizer')))
# currentpath = os.path.join(pathlib.Path(__file__).parent, '')

collectionId = -1


# Function for converting predefined table data into list for dropdownlist
def getList(tablename, collectionid): return util.convert_dbrow_list(
    db.getRowsOnFilters(tablename, {'collectionid =': '%s' % collectionid}))


# Function for fetching id (primary key) on name value
def getPrimaryKey(tableName, name, field='name'): return \
db.getRowsOnFilters(tableName, {' %s = ' % field: '"%s"' % name})[0][
    'id']  # return db.getRowsOnFilters(tableName, {' %s = ':'"%s"'%(field, name)})[0]['id']


def init(collection_id):
    # TODO function contract

    # Set collection id
    collectionId = collection_id
    c = collection_id

    # Define UI areas
    sg.theme('SystemDefault')
    greenArea = '#E8F4EA'  # Stable fields
    blueArea = '#99ccff'  # Variable fields
    greyArea = '#BFD1DF'  # Session & Settings

    defaultSize = (21, 1)  # Ensure element labels are the same size so that they line up
    element_size = (30, 1)  # Default width of all fields in the 'green area'
    blue_size = (28, 1)  # Default width of all fields in the 'blue area'

    font = ('Bahnschrift', 13)

    # TODO placeholder until higher taxonomic groups become available in SQLite
    taxonomicGroups = ['placeholder...']

    # Store elements in variables to make it easier to include and position in the frames
    storage = [sg.Text("Storage location:", size=defaultSize, background_color=greenArea, font=font),
               sg.Combo(getList('storage', c), key='cbxStorage', size=element_size, text_color='black',
                        background_color='white', font=('Arial', 12), readonly=True, enable_events=True), ]
    preparation = [sg.Text("Preparation type:", size=defaultSize, background_color=greenArea, font=font),
                   sg.Combo(getList('preptype', c), key='cbxPrepType', size=element_size, text_color='black',
                            background_color='white', font=('Arial', 12), readonly=True, enable_events=True), ]
    taxonomy = [sg.Text("Taxonomic group:", size=defaultSize, background_color=greenArea, font=font),
                sg.Combo(taxonomicGroups, key='cbxHigherTaxon', size=element_size, text_color='black',
                         background_color='white', font=('Arial', 12), readonly=True, enable_events=True), ]
    type_status = [sg.Text('Type status:', size=defaultSize, background_color=greenArea, font=font),
                   sg.Combo(getList('typeStatus', c), key='cbxTypeStatus', size=element_size, text_color='black',
                            background_color='white', font=('Arial', 12), readonly=True, enable_events=True), ]
    notes = [sg.Text('Notes', size=defaultSize, background_color=greenArea, font=font),
             sg.Multiline(size=(31, 5), background_color='white', text_color='black', key='txtNotes',
                          enable_events=False)]
    layout_greenarea = [storage, preparation, taxonomy, type_status, notes,
                        [sg.Checkbox('Multispecimen sheet', key='chkMultiSpecimen', background_color=greenArea,
                                     font=(11))], ]
    broadGeo = [
        sg.Text('Broad geographic region:', size=defaultSize, background_color=blueArea, text_color='black', font=font),
        sg.Combo(getList('georegion', c), size=blue_size, key='cbxGeoRegion', text_color='black',
                 background_color='white', font=('Arial', 12), readonly=True, enable_events=True), ]
    taxonInput = [
        sg.Text('Taxonomic name:     ', size=(21, 1), background_color=blueArea, text_color='black', font=font),
        sg.Input('', size=blue_size, key='txtTaxonName', text_color='black', background_color='white',
                 font=('Arial', 12), enable_events=True, pad=((5, 0), (0, 0))), ]
    taxonomicPicklist = [sg.Text('', size=defaultSize, background_color=blueArea, text_color='black', font=font),
                         sg.Listbox('', key='cbxTaxonName', select_mode='browse', size=(28, 6), text_color='black',
                                    background_color='white', font=('Arial', 12), enable_events=True,
                                    pad=((5, 0), (0, 0))), ]
    barcode = [sg.Text('Barcode:', size=defaultSize, background_color=blueArea, enable_events=True, text_color='black',
                       font=font),
               sg.InputText('', key='txtCatalogNumber', size=blue_size, text_color='black', background_color='white',
                            font=('Arial', 12), enable_events=True), ]
    # statusLabel = [sg.Text('Specimen record has been saved', font=('Arial', 20), size=(20, 5), justification='center',
    #                        background_color='#4f280a', text_color='yellow', key='texto')]

    layout_bluearea = [broadGeo, taxonInput, taxonomicPicklist, barcode,   # button_frame,
                       [sg.StatusBar('', relief=None, size=(32, 1), background_color=blueArea),
                        sg.Button('SAVE', key="btnSave", button_color='seagreen', bind_return_key=True),
                        sg.StatusBar('', relief=None, size=(20, 1), background_color=blueArea),
                        sg.Button('Go Back', key="btnBack", button_color='firebrick', pad=(120, 0))]]

    # column_left =

    loggedIn = [sg.Text('Logged in as:', size=defaultSize, background_color=greyArea, font=font),
                sg.Input(size=(24, 1), background_color='white', text_color='black',
                         readonly=True, key='txtUserName'), ]
    institution_ = [sg.Text('Institution:', size=defaultSize, background_color=greyArea, font=font),
                    sg.Input(size=(24, 1), background_color='white', text_color='black',
                             readonly=True, key="txtInstitution"), ]
    collections = [sg.Text('Collection:', size=defaultSize, background_color=greyArea, font=font),
                   sg.Input(size=(24, 1), background_color='white', text_color='black',
                            readonly=True, key="txtCollection"), ]
    work_station = [sg.Text('Workstation:', size=defaultSize, background_color=greyArea, font=font),
                    sg.Input(size=(24, 1), background_color='white', text_color='black',
                             readonly=True, key="txtWorkStation"), ]
    settings_ = [sg.Text('Settings ', size=defaultSize, justification='center', background_color=greyArea, font=14),
                 sg.Button('', image_filename='soptions_gear.png' , button_color=greyArea,
                           key='btnSettings', border_width=0)]
    horizontal_line = [sg.Text("_______________" * 5, background_color=greyArea)]  # horizontal line element hack
    layout_greyarea = [loggedIn, institution_, horizontal_line, collections, work_station, settings_,
                       [sg.Button('LOG OUT', key="btnLogout", button_color='grey40')]]

    # Combine elements into full layout
    # colLeft =
    confArea = [sg.Text('confirm', font=16)]
    # layout = [[sg.Frame('', [[sg.Column(layout_greenarea, background_color=greenArea)]], size=(250, 200), expand_x=True,
    #                     expand_y=True, background_color=greenArea),
    #            sg.Frame('', [[sg.Column(layout_greyarea, background_color=greyArea)]], size=(250, 300), expand_x=True,
    #                     expand_y=True, background_color=greyArea)],
    #           [sg.Frame('', [[sg.Column([layout_bluearea, confArea], background_color=blueArea)]], expand_x=False, expand_y=True,
    #                     background_color=blueArea, title_location=sg.TITLE_LOCATION_TOP)], ]

    greenFrame = sg.Frame('', [[sg.Column(layout_greenarea, background_color=greenArea)]], size=(250, 200), expand_x=True,
                        expand_y=True, background_color=greenArea)
    greyFrame = sg.Frame('', [[sg.Column(layout_greyarea, background_color=greyArea)]], size=(250, 300), expand_x=True,
                        expand_y=True, background_color=greyArea)
    blueFrame = sg.Frame('', [[sg.Column([layout_bluearea, confArea], background_color=blueArea)]], expand_x=False, expand_y=True,
                        background_color=blueArea, title_location=sg.TITLE_LOCATION_TOP)

    layout = [
                 [sg.Column(greenFrame, vertical_alignment='Top'), sg.VSeparator(),
         sg.Column(greyFrame, vertical_alignment='top')],
    ]

    window = sg.Window("TEST LAYOUT Mass Annotated Digitization Desk  (MADD)", layout, margins=(2, 2), size=(950, 580),
                       resizable=True, return_keyboard_events=True, finalize=True)

init(1)
