# from hashlib import new
import io, re, glob

chapter = ''
paragraph = True
book = ''
verseNumber = ''
newLine = ''
newChapter = True
title = ''
titleLine = False
bibleAsList = []
line = ''

def processVline():
    global chapter, paragraph, book, verseNumber, newLine, newChapter, title, titleLine, bibleAsList, line
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
    verseContent = verseContent.replace('\\f +', '<i><b>fn:</b> ')
    verseContent = verseContent.replace('\\f*', '</i>')               
    newLine += " " + verseContent
    if newChapter:
        newLine = re.sub(" <br>\n", '\n', newLine)
        newLine = re.sub('<br>(\d{1,3}:)', r'\n\1', newLine)
        bibleAsList.append(newLine)
        newLine = '' 
        newChapter = False


def turnUSFMintoTxt(filesLocation, uSLt):

    global chapter, paragraph, book, verseNumber, newLine, newChapter, title, titleLine, bibleAsList, line    
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
        line = ''

        lineNum = 0
        for line in bookLines:
            # there's a number of content lines that need to be merge together for accordance to work, but sometimes
            # a \li etc leads a blank line, other times it leads a line with text, this grabs both
            if (line.startswith('\\li') or line.startswith('\\q') or line.startswith('\\p')) and len(line) > 3:
                newLine = newLine.rstrip() + ' <br>' +  re.split('\s', line, 1)[1]    
            # the most common line, a verse line
            elif line.startswith('\\v'):
                # if it's not verse 1, we need to write the previous line and clear the newLine
                if not newChapter:
                    if newLine[-5:] == " <br>\n" or newLine[-5:] == " <br>": newLine = newLine[:-5] + '\n'
                    bibleAsList.append(newLine)
                    newLine = ''            
                verseNumber = re.split('\s', line)[1]
                # handle verse bridges, needs a little work because if the verse range has multiple lines, only the last verse will get it
                if verseNumber.find('-') > -1:
                    verseRange = verseNumber.split('-')
                    for x in range(int(verseRange[0]), int(verseRange[1]) + 1):
                        newLine += str(x) + " (" + verseRange[0] + "-" + verseRange[1] + ") "
                        processVline()                  
                else:        
                    newLine += verseNumber
                    processVline()
           # elif line == '\qs*': newLine += '\n'       
            elif (line.startswith('\\p') or line.startswith('\\q') or line.startswith(r'\\q\d')) and len(line) < 4:
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
        lineNum += 1

    with io.open("C:/Users/benja/Downloads/" + uSLt + ' for Accordance.txt', 'w', encoding='utf-8') as f:
        f.writelines(bibleAsList)

# turnUSFMintoTxt("C:/Users/benja/Downloads/ust/*.usfm", "UST")
turnUSFMintoTxt("C:/Users/benja/Downloads/ult/*.usfm", "ULT")