import io, re, glob

# testingfilepath = "c:/Users/benja/Downloads/ult/"
# testingfilename = "19-PSA.usfm"

def turnUSFMintoTxt(filesLocation, uSLt):

    #filesLocation = "C:/Users/benja/Downloads/ust/*.usfm"

    bibleAsList = []

    for filename in glob.glob(filesLocation):

        with io.open(filename, encoding='utf8') as f:
            bookLines = f.readlines()

        chapter = ''
        paragraph = True
        book = ''
        verseNumber = ''
        newLine = ''
        newChapter = True
        title = ''
        titleLine = False

        for line in bookLines:
            if line.startswith('\\v'):
                if not newChapter:
                    bibleAsList.append(newLine)
                    newLine = ''            
                verseNumber = re.split('\s', line)[1]
                if verseNumber.find('-') > -1:
                    verseRange = verseNumber.split('-')
                    for x in range(int(verseRange[0]), int(verseRange[1]) + 1):
                        newLine += str(x) + " (" + verseRange[0] + "-" + verseRange[1] + ") "
                        if len(title) > 0:
                            newLine += title
                            title = ''
                        if paragraph:
                            if not titleLine:
                                newLine += ' ¶'
                            else: 
                                newLine += ' <br>'
                                titleLine = False
                            paragraph = False
                        verseContent = re.split('\s', line, 2)[2]
                        verseContent = verseContent.replace('\\sp', '<br>')
                        verseContent = verseContent.replace('\\qs*', '')
                        verseContent = verseContent.replace('\\qs', ' ')
                        verseContent = verseContent.replace('\\q1', '<br>')
                        verseContent = verseContent.replace('\\q2', '<br>')
                        verseContent = verseContent.replace('\\q', '<br>')
                        verseContent = verseContent.replace('\\p', '<br>')
                        verseContent = verseContent.replace('\\li', '<br>')
                        verseContent = verseContent.replace('\\m', '<br>')
                        verseContent = verseContent.replace('\\f +', '<i><b>fn:</b> ')
                        verseContent = verseContent.replace('\\f*', '</i>')               
                        newLine += " " + verseContent
                        if newChapter:
                            bibleAsList.append(newLine)
                            newLine = '' 
                            newChapter = False
                    
                else:        
                    newLine += verseNumber
                    if len(title) > 0:
                        newLine += title
                        title = ''
                    if paragraph:
                        if not titleLine:
                            newLine += ' \u00B6'
                        else: 
                            newLine += ' <br>'
                            titleLine = False
                        paragraph = False
                    verseContent = re.split('\s', line, 2)[2]
                    verseContent = verseContent.replace('\\sp', '<br>')
                    verseContent = verseContent.replace('\\qs*', '')
                    verseContent = verseContent.replace('\\qs', ' ')
                    verseContent = verseContent.replace('\\q1', '<br>')
                    verseContent = verseContent.replace('\\q2', '<br>')
                    verseContent = verseContent.replace('\\q', '<br>')
                    verseContent = verseContent.replace('\\p', '<br>')
                    verseContent = verseContent.replace('\\li', '<br>')
                    verseContent = verseContent.replace('\\m', '<br>')
                    verseContent = verseContent.replace('\\f +', '<i><b>fn:</b> ')
                    verseContent = verseContent.replace('\\f*', '</i>')               
                    newLine += " " + verseContent
                    if newChapter:
                        bibleAsList.append(newLine)
                        newLine = '' 
                        newChapter = False
                    
            elif line.startswith('\\p') or line.startswith('\\q') or line.startswith(r'\\q\d'):
                paragraph = True

            elif line.startswith('\\d'): # include Psalm titles
                title = ' ¶ ' + re.split('\s', line, 1)[1].strip()
                titleLine = True
            elif re.split('\s', line)[0] == '\\c':
                chapter = re.split('\s', line)[1]
                newChapter = True
                newLine += chapter + ":"
            elif line.startswith('\\h'):
                book = re.split('\s', line, 1)[1]
                if book.startswith("Song"): book = "Song"
                if book[0] == '1' or book[0] == '2' or book[0] == '3':
                    book = book[0] + book[2:]
                newLine += book.strip() + ' '
        

    with io.open("C:/Users/benja/Downloads/" + uSLt + ' for Accordance.txt', 'w', encoding='ansi') as f:
        f.writelines(bibleAsList)

turnUSFMintoTxt("C:/Users/benja/Downloads/ust/*.usfm", "UST")
turnUSFMintoTxt("C:/Users/benja/Downloads/ult/*.usfm", "ULT")