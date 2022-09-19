import data_access as db


vv = db.getRows('specimen', limit=10)

for j in vv:
    print([item for item in j])

# bb = db.updateRow('specimen', 100, )
#
# UPDATE employees
# SET city = 'Toronto',
#     state = 'ON',
#     postalcode = 'M5P 2N7'
# WHERE
#     employeeid = 4;