from models import storage

stor = storage.Storage(29)

storageFields = stor.getFieldsAsDict()

print(storageFields)

locs = stor.loadPredefinedData()
locations = stor.storageLocations


def test_storage():
    assert locations[2][2] == 'Box 3'