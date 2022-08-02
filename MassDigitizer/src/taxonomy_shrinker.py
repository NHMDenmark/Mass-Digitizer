#For receiving dicts to be refined into greater accuracy


def refine_taxon_dict(the_dict, name_part):
    # Must refine dict according to the name_part string
    # returns smaller taxon dict

    new_taxonDict = {}
    name_length = len(name_part)
    print('in taxonomy_shrinker. Dict length = ', len(the_dict))
    for j in the_dict:

        if j[0:name_length] == name_part:

            new_taxonDict[j] = the_dict[j]

    return new_taxonDict

