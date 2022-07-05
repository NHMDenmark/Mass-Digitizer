#For receiving dicts to be refined into greater accuracy
import time


def refine_taxon_dict(the_dict, name_part):
    # Must refine dict according to the name_part string
    # returns smaller taxon dict

    new_taxonDict = {}
    name_length = len(name_part)
    for j in the_dict:

        if j[0:name_length] == name_part:
            # print('match of , ', j)
            new_taxonDict[j] = ''
    # taxon_dict[j[0]] = ''
    return new_taxonDict

#
# start2 = time.time()