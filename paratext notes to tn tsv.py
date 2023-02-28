from asyncio.windows_events import NULL
import io, os, random, re
idList = []

def makeNewID():
    abcs = "qwertyuioplkjhgfdsazxcvbnm" # quicker to type
    numbers = "1234567890"
    newID = ""
    isNotUniqueID = 1
    while isNotUniqueID != 0:
        newID = random.choice(abcs) + random.choice(abcs + numbers) + random.choice(abcs + numbers) + random.choice(abcs + numbers)
        isNotUniqueID = idList.count(newID)
        idList.append(newID)
    return newID

# CHANGE THIS to the path to your TN file, it might be in your downloads directory
filename = "C:/Users/benja/Documents/uwgit/en_tn/en_tn_19-PSA.tsv"

with io.open(filename, encoding='utf8') as f:
    for line in f:
        idList.append(line.split('\t')[1])

# txt file with paratext tns
filename = "C:/Users/benja/Downloads/tnsfromparatext.txt"

with io.open(filename, encoding='utf8') as f:
    inputdata = f.readlines()
    # output file:
with io.open(filename.replace('.txt','.tsv'), 'w', encoding='utf8', newline='\n') as newFile:
    ls = [None] * 9
    book= chapter= verse= SupportReference= OrigQuote= OccurrenceNote= nextline = ''
    for line in inputdata:
        # print(line)
        if len(line.strip()) == 0:
            if SupportReference != None:
                # Sometimes I put the SR before the ON, just checking that.
                if len(SupportReference) > len(OccurrenceNote):
                    sr = OccurrenceNote
                    OccurrenceNote = SupportReference
                    SupportReference = sr
            ls = [book, chapter, verse, makeNewID(), SupportReference, OrigQuote, '1', '', OccurrenceNote]
            print(ls)
            book= chapter= verse= SupportReference= OrigQuote= OccurrenceNote= nextline= ''
            # deal with any problems
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

            newLine = "\t".join(ls) + '\n'
            print(newLine)
            newFile.write(newLine)  

        elif re.search('^[1-3]?[A-Z]{2,3} ', line) != None:
            book, chapter, verse =  line.split(' ')[0], line.split(' ')[1].split(':')[0], line.split(' ')[1].split(':')[1].strip()
            nextline = 'origquote'
        elif nextline == 'origquote':
            OrigQuote = line.strip()
            nextline = "skip"
        elif nextline == "skip": 
            nextline = "note"
            continue
        elif nextline == "note":
            OccurrenceNote = line.strip()
            nextline = "supportref"
        elif nextline == "supportref":
            SupportReference = line.strip()                 



    
