# Create first dictionary
# dict1 = {  'Ritika': 5, 'Sam': 7, 'John' : 10 }
# # Create second dictionary
# dict2 = {'Aadi': 8,'Sam': [20, 22],'Mark' : 11 }

# def mergeDict(dict1, dict2):
#    ''' Merge dictionaries and keep values of common keys in list'''
#    dict3 = {**dict1, **dict2}
#    for key, value in dict3.items():
#        if key in dict1 and key in dict2:
#                dict3[key] = [value , dict1[key]]
#    return dict3
# # Merge dictionaries and add values of common keys in a list
# dict3 = mergeDict(dict1, dict2)
# print('Dictionary 3 :')
# print(dict3)

# from collections import defaultdict

# d1 = {1: 2, 3: 4}
# d2 = {1: 6, 3: [7, 9]}

# dd = defaultdict(list)

# for d in (d1, d2): # you can list as many input dicts as you want here
#     for key, value in d.items():
#         dd[key].append(value)
    
# print(dd) # result: defaultdict(<type 'list'>, {1: [2, 6], 3: [4, 7]})

# Merge lists of values when merging dictionaries
# possibleTranslations = [{'a': [1, 2, 3], 'b': [1, 2]}, {'c': [4, 5, 6, 7], 'a': [4, 5, 6], 'b': [3]}, {'c': [9, 7], 'd': [8]}, {'a': [3], 'b':[10,12]}]
possibleTranslations = [{"H1234.John": ['gen 1:23', 'exo 1:23'],"H1234.Sam": ['Lev 1:23', 'num 1:23'], "H1234.Jo": ['jos 1:23', 'jud 1:23'],"H1234.Peter": ['rut 1:23', '1sa 1:23']},{"H2345.Joe": ['Lev 1:23', '2sa 1:23'], "H2345.Sam": ['3sa 1:23', '4sa 1:23'], "H1234.John": ['mrk 1:23', 'mat 1:23']}]
newPossibleTranslations = {}
for nextDictionary in possibleTranslations:            
    for key, value in nextDictionary.items():
        if key in newPossibleTranslations:
            newPossibleTranslations[key].extend(value)
        else:
            newPossibleTranslations[key] = value
        # print(newPossibleTranslations)
print(newPossibleTranslations)
        # Returns: {'a': [1, 2, 3, 4, 5, 6], 'b': [1, 2], 'c': [4, 5, 6, 7]}