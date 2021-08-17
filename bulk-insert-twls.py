
import io, glob, os, csv, re, random

# testUSFM = "C://Users//benja//Documents//uwgit//hbo_uhb//02-EXO.usfm"
pathUSFM = "C://Users//benja//Documents//uwgit//hbo_uhb//"

# testTWL= "C://Users//benja//Documents//uwgit//en_twl//twl_EXO.tsv"
pathTWL= "C://Users//benja//Documents//uwgit//en_twl//"

wordStrongsGrabber = r"\\w (.*?)\|.*?strong=\"(?:\w?:?){0,2}(H\d{4})"
twbaselink = "rc://*/tw/dict/bible"
references = []
uniqueIDs = []
tags = []
origWords = []
occurrences = []
TWLinks = []

def makeLink(twarticle):
    # twarticle = input("Enter twarticle: ").lower().strip()
    with io.open("twlinksindex.txt", encoding='utf8') as f:
        twlinkslist = f.readlines()
    if '\n' not in twarticle: twarticle += '\n'
    if twbaselink + "/kt/" + twarticle  in twlinkslist:
        # print(twbaselink + "/kt/" + twarticle)
        return twbaselink + "/kt/" + twarticle, "keyterm"
    elif twbaselink + "/names/" + twarticle in twlinkslist:
        # print(twbaselink + "/names/" + twarticle)
        return twbaselink + "/names/" + twarticle, "name"
    elif twbaselink + "/other/" + twarticle in twlinkslist:
        # print(twbaselink + "/other/" + twarticle)
        return twbaselink + "/other/" + twarticle , ""
    else:
        raise Exception("article not found")

def makeNewID(idList):
    abcs = "qwertyuioplkjhgfdsazxcvbnm" # quicker to type
    numbers = "1234567890"
    newID = ""
    isNotUniqueID = 1
    while isNotUniqueID != 0:
        newID = random.choice(abcs) + random.choice(abcs + numbers) + random.choice(abcs + numbers) + random.choice(abcs + numbers)
        isNotUniqueID = idList.count(newID)
    return newID

def removeLinkAt(location):
    references.pop(location)
    uniqueIDs.pop(location)
    tags.pop(location)
    origWords.pop(location)
    occurrences.pop(location)
    TWLinks.pop(location)

def themainthing():
    strongs = input("Enter strong #: ").upper()
    linkToInsert, tagToInsert = makeLink(input("Enter twarticle: ").lower().strip())
    print("link will be: " + linkToInsert)
    totalInsertions = 0


    
    # TWLfile = [references, uniqueIDs, tags, origWords, occurrences, TWLinks]
    for filename in glob.glob(os.path.join(pathUSFM, '*.usfm')):

        references = []
        uniqueIDs = []
        tags = []
        origWords = []
        occurrences = []
        TWLinks = []
        currentBook = filename.split('-')[1].rstrip('.usfm') # from filename      
        # temp exclusions for other's work:
        exclusions = ["1KI"]
        if currentBook in exclusions: 
            print("excluding " + currentBook)
            continue

        currentChapter = 1
        currentVerse = 1

        f = open(filename, 'r', encoding='utf8')
        readf = f.read()
        f.close()
        if strongs not in readf:
            print("Not found in " + currentBook)
            continue
        else:       
            # print("found in " + currentBook)               
            insertionCount = 0  
            # it's easier to work with lists than a file

            currentTWLfile = pathTWL + 'twl_' + currentBook + '.tsv'

            with open(currentTWLfile, 'r', encoding='utf8') as f: 
                reader = csv.reader(f, delimiter = '\t')
                for reference, uniqueID, tag, origWord, occurrence, TWLink in reader:
                    references.append(reference.strip())
                    uniqueIDs.append(uniqueID)
                    tags.append(tag)
                    origWords.append(origWord)
                    occurrences.append(occurrence)
                    TWLinks.append(TWLink)
                    # return TWLfile
            originalTWLfileLength = len(references)
            with open(filename, 'r', encoding='utf8') as f:
                #matches = ()
                for line in f:
                    if line.find("\c") != -1 and line.find('\ca') == -1:
                        currentChapter = int(line.split('\c')[1].strip())
                        currentVerse = 1
                    elif line.find("v")  == 1 and line.find("va") == -1:
                        currentVerse = int(line.split("v")[1].strip())
                    elif line.find(strongs) != -1:
                        matches = re.findall(wordStrongsGrabber, line)
                        # print(matches)
                        if len(matches) > 0:                
                            for item in matches:
                                if item[1] == strongs:
                                    insertionIndex = 0
                                    tempVerse = currentVerse
                                    while insertionIndex == 0:      
                                        # print(TWLfile[0].index(str(currentChapter) + ":" + str(tempVerse-1)))                      
                                        if references.count(str(currentChapter) + ":" + str(tempVerse)) > 0:
                                            insertionIndex = references.index(str(currentChapter) + ":" + str(tempVerse))
                                            # print("this one worked " + currentBook+  str(currentChapter) + ":" + str(tempVerse))
                                        else: 
                                            # print("adding here " + currentBook+  str(currentChapter) + ":" + str(tempVerse))
                                            # print("insertion index: " + str(insertionIndex))
                                            tempVerse += 1
                                            #print(tempVerse)
                                        # it was in the last verse in a chapter, Ps119 has 170+ verses
                                        if tempVerse > 180:
                                            tempVerse = currentVerse - 1
                                            #print(currentBook+  str(currentChapter) + ":" + str(tempVerse))
                                            while insertionIndex == 0:
                                                # print(tempVerse)
                                                if references.count(str(currentChapter) + ":" + str(tempVerse)) > 0: 
                                                    # print("not true" + currentBook +  str(currentChapter) + ":" + str(tempVerse))
                                                    insertionIndex = references.index(str(currentChapter) + ":" + str(tempVerse)) + 1
                                                else:  # back up until we find an index
                                                    tempVerse -= 1

                                    # need to check for duplicates                
                                    testindex = insertionIndex
                                    makeTWL = True
                                    while references[testindex] == str(currentChapter)+ ":" + str(currentVerse):
                                        # if references[testindex] == str(currentChapter)+ ":" + str(currentVerse):
                                            # print(origWords[testindex])
                                        # print(currentBook + " " + str(currentChapter) + ":" + str(currentVerse)+ ": " + origWords[testindex] + "=?" + item[0])
                                        if origWords[testindex].strip() == item[0].strip(): # the text matches a TWL row content (strip is important!)
                                            makeTWL = False                         # so don't make a duplicate link                                                
                                                # this makes sure its not a case where I just wrote the article name
                                            if len(TWLinks[testindex].split("/")) == 1:                                            
                                                references.pop(testindex)
                                                uniqueIDs.pop(testindex)
                                                tags.pop(testindex)
                                                origWords.pop(testindex)
                                                occurrences.pop(testindex)
                                                TWLinks.pop(testindex)
                                                makeTWL = True

                                            # this next is the check for bad links (they point to invalid locations) (comparing kt/ephod with name/ephod or some such)
                                            elif TWLinks[testindex].split("/")[-1].strip() == linkToInsert.split("/")[-1].strip() and TWLinks[testindex].split("/")[-2].strip() != linkToInsert.split("/")[-2].strip() :
                                                print("improper link @ " + currentBook +  " " + str(currentChapter) + ":" + str(currentVerse) + ", found: " +TWLinks[testindex].split("/")[-2].strip() + "/" + TWLinks[testindex].split("/")[-1].strip() + " FIXING" )
                                                # removeLinkAt(testindex)
                                                references.pop(testindex)
                                                uniqueIDs.pop(testindex)
                                                tags.pop(testindex)
                                                origWords.pop(testindex)
                                                occurrences.pop(testindex)
                                                TWLinks.pop(testindex)
                                                makeTWL = True
                                            elif TWLinks[testindex].strip() != linkToInsert.strip(): # this just means you linked to something else, that's ok, but this script should mainly be used to update things you're pretty sure are always going to point to the same TW ariticle (so it goes to kt/sacrifice instead of kt/offering, that's a red flag that you shouldn't have scripted it)
                                                    print("link mismatch @ " + currentBook + " " + str(currentChapter) + ":" + str(currentVerse) + ", not overridden, found: " +TWLinks[testindex].strip().split("/")[-2] + "/" + TWLinks[testindex].strip().split("/")[-1] )
                                            break # we've decided to insert so let's not go back and say no
                                        else:  # otherwise keep working through exisiting TWLs
                                            testindex += 1
                                            if testindex > len(references) - 1: break
                                            continue
                                    
                                    if makeTWL:
                                        # print("inserted@ " + currentBook + " " + str(currentChapter) + ":" + str(currentVerse))
                                        insertionCount += 1
                                        references.insert(insertionIndex, str(currentChapter)+ ":" + str(currentVerse))
                                        uniqueIDs.insert(insertionIndex, makeNewID(uniqueIDs))
                                        tags.insert(insertionIndex, tagToInsert)
                                        origWords.insert(insertionIndex, item[0])
                                        occurrences.insert(insertionIndex, 1)
                                        TWLinks.insert(insertionIndex, linkToInsert.strip())

            if insertionCount > 0:
                totalInsertions += insertionCount
                os.rename(currentTWLfile, currentTWLfile.replace('.tsv','.old'))
                print("made " + str(insertionCount) + " insertions in " + currentBook)
                with open(currentTWLfile, 'w', encoding='utf8', newline='\n') as f:
                    i = 0   
                    while i < len(references):
                        twlWriter = csv.writer(f, delimiter = '\t')
                        twlWriter.writerow([references[i],uniqueIDs[i],tags[i],origWords[i],occurrences[i],TWLinks[i]])
                        i += 1
            else: 
              #  os.rename(currentTWLfile, currentTWLfile.replace('.tsv','.old'))
                print("no updates needed in " + currentBook)
    print("total updates: " + str(totalInsertions))

themainthing()