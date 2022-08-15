from asyncio.windows_events import NULL
import io, os, random, re
idList = []

def makeNewID(oldID):
    abcs = "qwertyuioplkjhgfdsazxcvbnm" # quicker to type
    numbers = "1234567890"
    newID = ""
    isNotUniqueID = 1
    while isNotUniqueID != 0:
        newID = random.choice(abcs) + random.choice(abcs + numbers) + random.choice(abcs + numbers) + random.choice(abcs + numbers)
        isNotUniqueID = idList.count(newID)
        print( "=>" + newID)
        idList.pop(oldID)
        idList.append(newID)
    return newID

# CHANGE THIS to the path to your TN file, it might be in your downloads directory
filename = "C:/Users/benja/Documents/uwgit/en_tn/en_tn_02-EXO.tsv"
os.rename(filename,filename.replace('.tsv','.old'))
filename = filename.replace('.tsv','.old')

with io.open(filename, encoding='utf8') as f:
    for line in f:
        idList.append(line.split('\t')[1])

with io.open(filename, encoding='utf8') as f:
    with io.open(filename.replace('.old','.tsv'), 'w', encoding='utf8', newline='\n') as newFile:
        for line in f:
            # fixes invisible whitespace
            newLine = line.replace('\u200c', '').replace('\u200b', '').replace('\u00A0', '') 

            ls = newLine.split('\t')

            # makes at the end of the note field from the support reference field
            if "-" in ls[4] and "[[rc:" not in ls[8]:   
                newOcNo = ls[8].rstrip() + " (See: [[rc://en/ta/man/translate/" + ls[4].strip() + "]])\n"
                ls[8] = newOcNo
            # fixing more white space issues
            tab = 0
            while tab < len(ls): 
                ls[tab] = ls[tab].strip()
                ls[tab] = ls[tab].strip('\u2060')
                tab += 1

            # origquote should not have spaces around …
            ls[5] = ls[5].replace("...", "…") # not 3 dots
            ls[5] = ls[5].replace(" … ", "…")
            ls[5] = ls[5].replace("… ", "…")
            ls[5] = ls[5].replace(" …", "…")

            # however, note field should
            ls[8] = ls[8].replace("(…/", "(../") # fix for a possible error
            ls[8] = ls[8].replace("...", "…") # not 3 dots
            splitOnEllipsis = 0
            splitOnEllipsis = ls[8].split("…")
            for a in range(len(splitOnEllipsis)): splitOnEllipsis[a] = splitOnEllipsis[a].strip() # don't want two spaces in all the places its already correct
            if len(splitOnEllipsis) > 1: ls[8] = " … ".join(splitOnEllipsis)
                 
            # notes that are just ATs should still say Alternate translation: “blah”
            if ls[8].startswith('“'): ls[8] = "Alternate translation: " + ls[8]

            # apparently markdown headers need spacing - dumb
            # if ls[1] == "2":
            if ls[2] == "intro":
                introLines = ls[8].split("<br>")
                # for a in introLines: print(a)
                # print("–––––––––––––––")
                L = 0
                while L < len(introLines):
                    if introLines[L].startswith("#"):
                        if L+1  == len(introLines):
                            introLines.insert(L+1,'')
                        elif introLines[L+1] != '': 
                            introLines.insert(L+1,'')
                        if L != 0:
                            if introLines[L-1] != '': introLines.insert(L,'')    
                    # don't need three <br> in a row
                    elif introLines[L] == '':
                        if L != 0 and L+1 < len(introLines):
                            if introLines[L+1] == '' and introLines[L-1] == '': introLines.pop(L)
                    L += 1
                ls[8] = "<br>".join(introLines)
                # for a in introLines: print(a)
                    

            # making sure id field is unique (should only happen once per file checked)
            if ls[3][0].isdigit(): 
                ls[3] = makeNewID(ls[3])

            newLine = "\t".join(ls) + '\n'
            newFile.write(newLine)
