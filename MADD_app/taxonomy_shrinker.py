#For receiving dicts to be refined into greater accuracy
import time


def refine_taxon_dict(theDict, name_part):
    #Must refine dict according to the name_part string
    #returns smaller taxon dict
    new_taxonDict = {}

#
# input_field = 'Cor'
# query = "SELECT pow.taxon_name from pow WHERE pow.taxon_name LIKE '{}%';".format(input_field)
# start = time.time()
# out = cur.execute(query)
    end = time.time()

    for j in theDict:
        # print(j, j[0:4])

        if j[0:4] == name_part:
            print('match of , ', j)
            new_taxonDict[j] = ''
    # taxon_dict[j[0]] = ''
    return new_taxonDict
# pprint(taxon_dict)
# print(len(taxon_dict))
# input_field = 'Cora'
#
# start2 = time.time()
# keys = taxon_dict.keys()
# res = any(key.startswith(input_field) for key in taxon_dict)
# print(res)
# candidates = [elem for elem in keys if elem[0:4] == input_field]
# end2 = time.time()
# print(candidates)
# print(len(candidates))
# print('exe dicts = ', end2 - start2)