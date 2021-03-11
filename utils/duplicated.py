# Removes duplicates from a list

def removeDuplicate(listing):
    preRemove = len(listing)
    newList = list(dict.fromkeys(listing))
    print("Duplicates found: " + str(preRemove - len(newList)))
    return newList


def removeDuplicates(listing, purpose):
    preRemove = len(listing)
    newList = list(dict.fromkeys(listing))
    print("\t" + purpose + " duplicates found: " + str(preRemove - len(newList)))
    return newList
