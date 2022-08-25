import io, glob, re

def processVline(verseNumber, verseText):
    global paragraph
    # if verseNumber == '1' and paragraph: print(verseText)
    if verseText.startswith(' <br>'): verseText = verseText[6:]
    # insert a paragraph marker if needed
    if paragraph:                
        newVerseContent = verseNumber + " ¶ " + verseText
        paragraph = False
    else: newVerseContent = verseNumber + " " + verseText
    # find out if this line marks a new paragraph, if so, remove the trailing <br> and mark for a paragraph
    while newVerseContent.rstrip().endswith('<br>'):
        newVerseContent = newVerseContent.rstrip()[:-4]
        paragraph = True
    return newVerseContent


def addToBibleAsList(text, withNewLine):
    global bibleAsList
    bibleAsList.append(text) if withNewLine else bibleAsList.append(text.rstrip())

def turnUSFMintoTxt(filesLocation, uSLt):

    global bibleAsList

    bibleAsList = []
    for filename in glob.glob(filesLocation):

        with io.open(filename, encoding='utf8') as f:
            bookLines = f.readlines()

        for index, elem in enumerate(bookLines):
            
            if index + 1 < len(bookLines) and index - 1 >= 0: 
                
                if bookLines[index+1].startswith(r'\c ') or bookLines[index+1].startswith(r'\v')  or bookLines[index+1].startswith(r'\h') or bookLines[index+1].startswith(r'\toc1'):
                    addToBibleAsList(elem, True)       
                        # work from here, I think this might be right, but how to append /v 1 to /c lines with minimal processing is a question...
                        # and then i want something that only appends if the line starts with /c /v or /h
                else:       
                    addToBibleAsList(elem, False) 
                
        bibleAsList.append('\n')
    flatBible = ''
    accordanceModifiedList = []
    global paragraph 
    paragraph= False
    for line in bibleAsList:
        flatBible += line
    
    for line in flatBible.split('\n'):
        verseContent = line
        verseContent = verseContent.replace('\\sp', ' <br>')
        verseContent = verseContent.replace('\\qs*', '')
        verseContent = verseContent.replace('\\qs', ' ')
        verseContent = verseContent.replace('\\q1', ' <br>')
        verseContent = verseContent.replace('\\q2', ' <br>')
        verseContent = verseContent.replace('\\q3', ' <br>')
        verseContent = verseContent.replace('\\q', ' <br>')
        verseContent = verseContent.replace('\\pi2', ' <br>')
        verseContent = verseContent.replace('\\pi', ' <br>')        
        verseContent = verseContent.replace('\\p', ' <br>')
        verseContent = verseContent.replace('\\li', ' <br>')
        verseContent = verseContent.replace('\\m', ' <br>')
        verseContent = verseContent.replace('\\m', ' <br>')
        verseContent = verseContent.replace('\\f +', '<i><b>fn:</b> ')
        verseContent = verseContent.replace('\\f*', '</i>')
        # I want to filter out lines that I don't need
        if verseContent.startswith(r'\v '):
            # drop the \v 
            newVerseContent = verseContent[3:]
            # split the line into verse number and the text
            verseNumber, verseText = re.split('\s', newVerseContent, 1)
            if verseNumber == '1': 
                newVerseContent = processVline('', verseText)
                accordanceModifiedList.append(newVerseContent.strip() + '\n')
            elif verseNumber.find('-') > -1:
                verseRange = verseNumber.split('-')
                becomesParagraph = False
                for x in range(int(verseRange[0]), int(verseRange[1]) + 1):
                    verseNumber = str(x) + " (" + verseRange[0] + "-" + verseRange[1] + ") "
                    newVerseContent = processVline(verseNumber, verseText)     
                    accordanceModifiedList.append(newVerseContent.strip() + '\n')                      
                    if paragraph: becomesParagraph = True
                    paragraph = False
                paragraph = becomesParagraph
            else:   
                newVerseContent = processVline(verseNumber, verseText)
                accordanceModifiedList.append(newVerseContent.strip() + '\n')                        

        # chapter lines
        elif verseContent.startswith('\c '):
            chapter = re.findall(r"\\c (\d{1,3})", verseContent)[0]
            if re.search(r'<br>', verseContent):
                paragraph = True
                #print(verseContent)
            newVerseContent = chapter + ":1 " if chapter != '1' else " " + chapter + ":1 "
            split = verseContent.split(r'\d')
            if len(split) > 1:
                newVerseContent += split[1]
            split = verseContent.split(r'\sp')
            if len(split) > 1:
                newVerseContent += '<br>' + split[1] + '<br>'
            accordanceModifiedList.append(newVerseContent) 
                    
        elif verseContent.startswith('\h '):
            # previously I needed a line break after \h (title) b/c there were several extra usfm lines, now i want it on the same line with 1:1
            book = re.split(r'\\', line[3:], 1)[0]
            if book.startswith("Song"): book = "Song"
            if book[0] == '1' or book[0] == '2' or book[0] == '3':
                book = book[0] + book[2:]
            
            accordanceModifiedList.append(book)
            # a new book will always start with a new paragraph
            paragraph = True
    if uSLt == 'UGNT' or uSLt == 'UHB':
        for index, elem in enumerate(accordanceModifiedList):
            accordanceModifiedList[index] = re.sub('¶', '', elem)        
    with io.open("C:/Users/benja/Downloads/" + uSLt + ' for Accordance.txt', 'w', encoding='utf-8') as f:
        f.writelines(accordanceModifiedList)

turnUSFMintoTxt("C:/Users/benja/Downloads/ust/*.usfm", "UST")
turnUSFMintoTxt("C:/Users/benja/Downloads/ult/*.usfm", "ULT")         
turnUSFMintoTxt("C:/Users/benja/Downloads/uhb/*.usfm", "UHB")   
turnUSFMintoTxt("C:/Users/benja/Downloads/ugnt/*.usfm", "UGNT")   