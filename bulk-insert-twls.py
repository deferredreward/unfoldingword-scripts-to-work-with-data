
import io, glob, os, csv, re, random

testUSFM = "C://Users//benja//Documents//uwgit//hbo_uhb//02-EXO.usfm"
testTWL= "C://Users//benja//Documents//uwgit//en_twl//twl_EXO.tsv"

wordStrongsGrabber = r"\\w (\W*)\|.*?strong=\"(?:\w?:?){0,2}(H\d{4})"
twbaselink = "rc://*/tw/dict/bible/"

def makeLink():
    twarticle = input("Enter twarticle: ")
    with io.open("twlinksindex.txt", encoding='utf8') as f:
        twlinkslist = f.readlines()

    if twbaselink + "/kt/" + twarticle  in twlinkslist:
        return twbaselink + "/kt/" + twarticle
    elif twbaselink + "/names/" + twarticle in twlinkslist:
        return twbaselink + "/names/" + twarticle
    elif twbaselink + "/other/" + twarticle in twlinkslist:
        return twbaselink + "/other/" +twarticle    


references = []
uniqueIDs = []
tags = []
origWords = []
occurrences = []
TWLinks = []
# I'm making a list of lists because they represent rows so TWLfile[anyindex][5] is row 6 (5th of content)
TWLfile = [references, uniqueIDs, tags, origWords, occurrences, TWLinks]

# it's easier to work with lists than a file
with open(testTWL, 'r', encoding='utf8') as f: 
    reader = csv.reader(f, delimiter = '\t')
    for reference, uniqueID, tag, origWord, occurrence, TWLink in reader:
        references.append(reference)
        uniqueIDs.append(uniqueID)
        tags.append(tag)
        origWords.append(origWord)
        occurrences.append(occurrence)
        TWLinks.append(TWLink)

def makeNewID():
    abcs = "qwertyuioplkjhgfdsazxcvbnm" # quicker to type
    numbers = "1234567890"
    newID = ""
    isNotUniqueID = 1
    while isNotUniqueID != 0:
        newID = random.choice(abcs) + random.choice(abcs + numbers) + random.choice(abcs + numbers) + random.choice(abcs + numbers)
        isNotUniqueID = TWLfile[1].count(newID)
    return newID
        # if isNotUniqueID != 0:
        #     print(newID +  "is a duplicate of line " + str(TWLfile[1].index(newID)))
        # else:
        #     print(newID)
   

# try:
#     print(TWLfile[0].index("1:23"))
# except: print("invalid verse or no twl")