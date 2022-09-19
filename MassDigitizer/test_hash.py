import hashlib

#
# hashlib.md5().update(str(123456789).encode("utf-8"))
# print(hashlib.md5().hexdigest())
# print(hashlib.md5().hexdigest()[:10])

#
one = '123456789'
# ohash = str(hash(one))
#
# print(ohash)

hashList = []
lenlist = []

for j in range(10):
    item = hash(str(j))
    sliced = str(item)[2:18]
    hashList.append(item)
    lenlist.append(len(sliced))

print(hashList)
print(lenlist)
def checkIfDuplicates_2(listOfElems):
    ''' Check if given list contains any duplicates '''
    setOfElems = set()
    counter = 0
    for elem in listOfElems:
        if elem in setOfElems:
            counter += 1
            return True, elem
        else:
            setOfElems.add(elem)
    return False

res = checkIfDuplicates_2(hashList)
print(res)
# print(hashList)