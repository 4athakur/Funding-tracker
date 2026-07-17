a=['a','b','c',2]
aa=['d','e','c',2]

def common_items(list1, list2):
    set2 = set(list2)   # convert to set for fast lookup
    return [i for i in list1 if i in set2]

print(common_items(a,aa))