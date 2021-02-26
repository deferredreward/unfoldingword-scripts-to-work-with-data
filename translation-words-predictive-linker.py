import re, csv, io, datetime, os, glob

twLink = "x-tw=\"rc://*/tw/dict/bible/"
wordGrabber = r"strong=\"(?:\w?:?){0,2}(H\d{4})\w?\".+?(?:((?:names|other|kt)\/\w+)|\\w)"
BPrefs = '.\\BPrefs'
BPsToUpdate = '.\\BPsToUpdate'

# list = [["H1234","other/slain", 5],["H2468","kt/sacrifice", 3]]

sLinkPairs =[]
for filename in glob.glob(os.path.join(BPrefs, '*.usfm')):
    with io.open(filename, encoding='utf8') as f:  # open zfile
        for x in f:
            matches = re.findall(wordGrabber, f.readline()) 
            # matches is a list of  tuples w/ strongs & twlinks: [('H3068', 'kt/yahweh'), ('H4410', 'other/kingdom')]
            for y in matches:  
                if len(y[1]) > 0:
                    l = [ y[0], y[1] ]
                    sLinkPairs.append(l)

# I now have an intermediate list, I may be able to put the next code into what's above, but for now, conceptually it helps to break it into more steps
            
sLinkPairsWithCount = []

for l in sLinkPairs:
    c = sLinkPairs.count(l) # so now I know how many ['H6215', 'names/esau'] or some such I have
    sLPWC = [l[0], l[1], c] # make a list with the data
    if not sLPWC in sLinkPairsWithCount:
        sLinkPairsWithCount.append(sLPWC)
sLinkPairsWithCount.sort()
# So now I have something like this (but sorted!):
# ['H3130', 'names/josephot', 3]
# ['H4714', 'names/egypt', 70]
# ['H3478', 'kt/israel', 87]

dropList=[] # a list of the items that need to be removed
for row in range(len(sLinkPairsWithCount)-1):
    dup = 1
    # dupList is a temporary list of duplicates like:
    # [['H7725', 'kt/restore', 2], ['H7725', 'kt/return', 1], ['H7725', 'other/return', 8], ['H7725', 'other/turn', 3]]
    dupList = [sLinkPairsWithCount[row]]  # initially: [['H7725', 'kt/restore', 2]]
    # checks if the strongs# is the same for the next item in the LinkPair list
    while sLinkPairsWithCount[row][0] == sLinkPairsWithCount[row+dup][0]: 
        dupList.append(sLinkPairsWithCount[row+dup]) # if so add it: [['H7725', 'kt/restore', 2], ['H7725', 'kt/return', 1]]
        dup+=1
    if len(dupList) > 1: # if there's multiple values
        # print(dupList)
        highestCount = 0
        keepThisOne = 0
        # we need to find the most used link
        for item in range(len(dupList)):
            # if this item isn't on the master dropList, add it
            if dupList[item] not in dropList:
                dropList.append(dupList[item])
            # then, see if it is used more than the others 
            if dupList[item][2] > highestCount: # 2>0?,1>2?,8>2?,3>8?
                highestCount = dupList[item][2] # 0 >> 2 >> 8
                keepThisOne = item # 0 > 0 > 2
        # this has to be outside the for loop or we remove the middle 2-3 items from the  list
        dropList.remove(dupList[keepThisOne]) # ok so we'll keep ['H7725', 'other/return', 8] by removing it from the dropList
      
# dropList.sort()
# print(dropList)
# print(len(dropList))

# Make a copy of the original list and drop the lower ranked tW links
# I probably could just have generated this list above
sMostLinkedTo = sLinkPairsWithCount.copy()
for i in dropList:
    sMostLinkedTo.remove(i)

# Now let's drop the low numbers
# 1 match, drop unless name/
# < 5 matches, drop if not kt/
for lp in sMostLinkedTo:
    if lp[2] == 1 and not lp[1].startswith("name"):
        sMostLinkedTo.remove(lp)
    elif lp[2] < 5 and not lp[1].startswith("kt"):
        sMostLinkedTo.remove(lp)

# Now I need this list without the count, so revert to: ['H7725', 'other/return']
sMostLinkedToWithoutCount = {}
for i in range(len(sMostLinkedTo)):
    sMostLinkedToWithoutCount.update({sMostLinkedTo[i][0]: sMostLinkedTo[i][1]})

issues = ["H5921","H3212"]
for i in issues:
    if i in sMostLinkedToWithoutCount:
        sMostLinkedToWithoutCount.pop(i)

# print(sMostLinkedToWithoutCount)
# print(len(sLinkPairsWithCount))
# print(len(sMostLinkedTo))
# print(len(sMostLinkedToWithoutCount))

""" Now, to edit the other usfm files 
carefully

twLink = "x-tw=\"rc://*/tw/dict/bible/"
wordGrabber = r"strong=\"(?:\w?:?){0,2}(H\d{4})\w?\".+?(?:((?:names|other|kt)\/\w+)|\\w)"
BPrefs = '.\BPrefs'
BPsToUpdate = '.\BPsToUpdate'
"""

sLinkPairs =[]
notword =0
oneoftwotwlink = 0
doubletwlink = 0
alreadytwlink=0
madeupdate = 0
notmatch = 0
forloop = 0
for filename in glob.glob(os.path.join(BPsToUpdate, '*.usfm')):
    updatesSubtotal = madeupdate
    with io.open(filename, 'r', encoding='utf8') as oldFile:  # open a file to read
        newfilename = filename.replace('.usfm','-new.usfm')
        with io.open(newfilename, 'w', encoding='utf8', newline='\n') as newFile:  # open a file to write
            for line in oldFile:
                line = line.replace('  ',' ')
                newLineContent = line
                forloop += 1
                # if the line isn't a word, write it to the new file and move on
                if not line.startswith('\w'):
                    newFile.write(line)
                    notword +=1
                    continue                 
                # matches is a list of  tuples w/ strongs & twlinks: [('H3068', 'kt/yahweh'), ('H4410', 'other/kingdom')]
                matches = re.findall(wordGrabber, line) 
                lenmatches = len(matches)
                # if there's already a tw-link, write the line to the new file and move on

                if lenmatches == 1 and len(matches[0][1]) > 1:
                    newFile.write(line)
                    alreadytwlink += 1
                    continue               
               # double tw-link, rare I think                         
                if lenmatches == 2 and len(matches[0][1]) > 1 and len(matches[1][1]) > 1:
                    newFile.write(line)
                    doubletwlink += 1
                    continue           
                # if item 1 matches and item 2 doesn't                
                if lenmatches == 2 and len(matches[0][1]) > 1 and len(matches[1][1]) == 0:
                    newFile.write(line)
                    oneoftwotwlink += 1
                    continue 
                # item 2 matches and item 1 doesn't
                if lenmatches == 2 and len(matches[0][1]) == 0 and len(matches[1][1]) > 1:
                    newFile.write(line)
                    oneoftwotwlink += 1
                    continue         
      

                # Ok, here we make updates           
                # If we have a single term and a single match
                if lenmatches == 1  and matches[0][0] in sMostLinkedToWithoutCount:
                    dividedLine = line.split('\w*')
                    newLineContent = dividedLine[0] + ' ' + twLink+sMostLinkedToWithoutCount[matches[0][0]] + '"\w*' + dividedLine[1]          
                    if  "־\w" in line:
                        newLineContent += "\w*"
                        # print("1:1")
                        # print("0:" + dividedLine[0])
                        # print("1:" + dividedLine[1])
                        # print("2:" + dividedLine[2])
                        # print("NL:" + newLineContent)                          
                    newFile.write(newLineContent)
                    madeupdate +=1
              
                    continue
                # if we match the second item
                if lenmatches == 2  and matches[0][0] not in sMostLinkedToWithoutCount and matches[1][0] in sMostLinkedToWithoutCount:
                    dividedLine = line.split('\w*')
                    newLineContent = dividedLine[0] + '\w*' + dividedLine[1] + ' ' + twLink+sMostLinkedToWithoutCount[matches[1][0]] + '"\w*' + dividedLine[2]
                    newFile.write(newLineContent)
                    madeupdate +=1
                    continue
                # if we match the first item
                if lenmatches == 2  and matches[0][0] in sMostLinkedToWithoutCount and matches[1][0] not in sMostLinkedToWithoutCount:
                    dividedLine = line.split('\w*')
                    newLineContent = dividedLine[0] + ' ' + twLink+sMostLinkedToWithoutCount[matches[0][0]] + '"\w*' + dividedLine[1] +  '\w*' + dividedLine[2]
                    newFile.write(newLineContent)
                    madeupdate +=1
                    continue                

                # if we have a double match, rare
                if lenmatches == 2  and matches[0][0] in sMostLinkedToWithoutCount and matches[1][0] in sMostLinkedToWithoutCount:
                    dividedLine = line.split('\w*')
                    newLineContent = dividedLine[0] + ' ' + twLink+sMostLinkedToWithoutCount[matches[0][0]] + '"\w*' + dividedLine[1] + ' ' + twLink+sMostLinkedToWithoutCount[matches[1][0]] + '"\w*' + dividedLine[2]
                    newFile.write(newLineContent)                    
                    madeupdate +=1
                    continue

                # like a switch: default
                newFile.write(line)
                notmatch+=1
    print("Made " + str(madeupdate-updatesSubtotal) + " updates to " + filename.split('\\')[2])


print("not words: " + str(notword))
print("alreadytwlink: " + str(alreadytwlink))
print("oneoftwotwlink: " + str(oneoftwotwlink))
print("doubletwlink: " + str(doubletwlink))
print("madeupdate: " + str(madeupdate))
print("no match: " + str(notmatch))
print("lines: " + str(notword+alreadytwlink+madeupdate+notmatch+doubletwlink+oneoftwotwlink))
print("for loop ran: " + str(forloop))
                






# This creates a tsv output of the results for manual checking
outFile = "output" + str(datetime.datetime.now()).replace(":",".") + ".tsv"

f_output =open(outFile, 'w', newline='')
for r in sLinkPairsWithCount:
    tsv_output = csv.writer(f_output, delimiter='\t')
    tsv_output.writerow(r)

f_output.close()


def str2unix(input_str: str) -> str:
    r"""
    Converts the string from \r\n line endings to \n

    Parameters
    ----------
    input_str
        The string whose line endings will be converted

    Returns
    -------
        The converted string
    """
    r_str = input_str.replace('\r\n', '\n')
    return r_str