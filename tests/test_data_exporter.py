import data_exporter
import pytest


def test_exportSpecimens():
    export_file = data_exporter.exportSpecimens('xlsx')
    print('¤¤¤¤¤¤¤'+export_file)
    assert export_file == 'No specimen records to export.'

def test_generteFilename():
    export_path = data_exporter.generateFilename('my_specimens', 'xlsx',
                                                 r"C:\Users\bxq762\Documents\workspace\Mass digitizer\DaSSCo\MassDigitizer\output")
    print('%%%%%%%'+export_path)
    assert export_path

test_exportSpecimens()
test_generteFilename()