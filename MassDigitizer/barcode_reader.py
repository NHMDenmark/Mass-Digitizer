import sys
import PySimpleGUI as sg


# mybar = input('getting the barcode with ice :)')


layout = [[sg.Input('', key="brcBarcode", size=(18,1), enable_events=True)]]

window = sg.Window('barcode crawl', layout, finalize=True)
entry_barcode = window['brcBarcode']
entry_barcode.bind("<Return>", "_RETURN")

barcodeList = []
while True:
    event, values = window.read()
    if event == "brcBarcode_RETURN":
        print(f"Input barcode: {values['brcBarcode']}")

    if event == sg.WINDOW_CLOSED:
        break

window.close()
