import PySimpleGUI as sg

# Internal 
import data_access as db
import util

collections = db.getRows('collection')
collList = util.convert_dbrow_list(collections)

layout = [[sg.Text('collections'), sg.Combo(collList, enable_events=True, key='cbxCollections', size=(30, 1))],]
window = sg.Window('testing', layout)

while True:
    event, values = window.read()
    if event == sg.WINDOW_CLOSED:
        break
    elif event =='cbxCollections':
        text = values[event]
        index = window[event].widget.current()
        id = collections[index]['id'] 
        spid = collections[index]['spid'] 
        print(index, id, spid, repr(values[event]))

window.close()