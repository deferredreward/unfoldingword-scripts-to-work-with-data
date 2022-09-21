from datetime import datetime
from email.quoprimime import quote
from operator import contains
import re, glob


brokenbooks = []

TNfilesLocation = "C:/Users/benja/Documents/uwgit/en_tn/*.tsv"
ULTfilesLocation = "C:/Users/benja/Downloads/ult/"
TAfilesLocation = "C:/Users/benja/Documents/uwgit/en_ta/translate/"


now = datetime.now().strftime("%Y-%m-%dT%H:%M:%S")
opener = [
    '<?xml version="1.0" encoding="utf-8"?>',
    '<CommentList>',
    '<Comment Thread="LicenseInfo" User="Benjamin Wright" VerseRef="GEN 1:0" Language="en-US" Date="{now}">',
    "<SelectedText />",
    "<StartPosition>0</StartPosition>",
    "<ContextBefore></ContextBefore>",
    "<ContextAfter></ContextAfter>",
    "<Status></Status>",
    "<Type></Type>",
    "<ConflictType />",
    "<Verse></Verse>",
    "<ReplyToUser />",
    "<HideInTextWindow>true</HideInTextWindow>",
    '<Contents>unfoldingWord Translation Notes released under CC BY SA 4.0</Contents>',
    '</Comment>']

with open("C:/My Paratext 9 Projects/ULT/Notes_Benjamin Wright.xml", mode='w', encoding='utf8') as notesFile:
     for line in opener:
        notesFile.write(f'{line}\n')

booksToCheck = [
    "GEN",
    "EXO",
    "LEV",
    # "NUM",
    "DEU",
    "JOS",
    "JDG",
    "RUT" ,
    "1SA",
    "2SA",
    "1KI",
    "2KI",
    "1CH",
    "2CH",
    "EZR",
    "NEH",
    "EST",
    "JOB",
    "PSA",
    "PRO",
    "ECC",
    "SNG",
    "ISA",
    "JER",
    "LAM",
    "EZK",
    "DAN",
    "HOS",
    "JOL",
    "AMO",
    "OBA",
    "JON",
    "MIC",
    "NAM",
    "HAB",
    "ZEP",
    "HAG",
    "ZEC",
    "MAL",
        
     "MAT",
    "MRK",
    "LUK",
    "JHN",
    "ACT",
    "ROM",
    "1CO",
    "2CO", 
    "GAL",
    "EPH",
    "PHP",
    "COL",
    "1TH",
    "2TH",
    "1TI",
    "2TI",
    "TIT",
    "PHM",
    "HEB",
    "JAS",
    "1PE",
    "2PE",
    "1JN",
    "2JN",
    "3JN",
    "JUD",
    "REV"
]


for TNfile in glob.glob(TNfilesLocation):
    # with open("C:/My Paratext 9 Projects/ULT/Notes_Benjamin Wright.xml", mode='w', encoding='utf8') as notesFile:
    #     for line in opener:
    #         notesFile.write(f'{line}\n')

    xmlOutput = []
    bookLoc = TNfile.split('_')[-1].replace('tsv','usfm')
    print(bookLoc[3:6])
    if bookLoc[3:6] not in booksToCheck: continue

    with open(TNfile, encoding = 'utf8')as tnFile:
        tnFile.readline()
        tNotes = tnFile.readlines()
    with open(ULTfilesLocation + bookLoc, encoding='utf8') as scriptureFile:
        scriptureBook = scriptureFile.readlines()

    
    


    for note in tNotes:
        now = datetime.now().strftime("%Y-%m-%dT%H:%M:%S.%f")
        if len(note.split('\t')) != 9:
            print(bookLoc)
            print(note)
            continue
        Book, Chapter, Verse, tcID, SupportReference, OrigQuote, Occurrence, GLQuote,OccurrenceNote = note.split('\t')
        OccurrenceNote = OccurrenceNote.replace('<br><br>', '<br />')
        OccurrenceNote = OccurrenceNote.replace('<br>', '<br />')
        OccurrenceNote = re.sub(r'\*\*(.*?)\*\*', r'<bold>\1</bold>', OccurrenceNote)
        taArticle = re.findall(r'\[\[rc:\/\/en\/ta\/man\/translate/(.*?)]]', OccurrenceNote)
        if len(taArticle) > 0:
            taArticle = taArticle[0]
            taArticleTitle = ''
            try: 
                with open(TAfilesLocation + taArticle + "/title.md", encoding = 'utf8') as taTitle:
                    taArticleTitle = taTitle.readline()
            except: taArticleTitle = taArticle
            OccurrenceNote = re.sub(r'\[\[rc:\/\/en\/ta\/man\/translate/(.*?)]]', taArticleTitle + r' at https://git.door43.org/unfoldingWord/en_ta/src/branch/master/translate/\1/01.md', OccurrenceNote)
        OccurrenceNote = OccurrenceNote.replace('&', 'and')
        if Chapter == 'front' : Chapter = '1'
        if  Verse == 'intro': Verse = '0'
        if Chapter != '0' and Verse != '0':
            chapterStart = scriptureBook.index(f'\c {Chapter}\n')
            verseLocation = chapterStart + 1
            foundVerse = False
            while not foundVerse and verseLocation < len(scriptureBook):
                if scriptureBook[verseLocation].startswith(f'\\v {Verse} '): 
                    foundVerse = True
                else: verseLocation += 1
            verseContent = scriptureBook[verseLocation].split(' ', 2)[2]
        else: verseContent = ''

        xmlOutput.append(f'<Comment Thread="{tcID}" User="unfoldingWord" VerseRef="{Book} {Chapter}:{Verse}" Language="en-US" Date="{now}">')
        if len(GLQuote) == 0: 
            xmlOutput.append("<SelectedText />")
            xmlOutput.append("<StartPosition>0</StartPosition>")
            xmlOutput.append("<ContextBefore></ContextBefore>")
            xmlOutput.append(f"<ContextAfter>{verseContent}</ContextAfter>")
        else:
            if contains(verseContent, GLQuote):
                quoteStart = verseContent.index(GLQuote)
                quoteFinish = quoteStart + len(GLQuote) + 1
                contextBefore = verseContent[:quoteStart]
                contextAfter = verseContent[quoteFinish:]
                xmlOutput.append(f"<SelectedText> {GLQuote} </SelectedText>")
            else: 
                quoteStart = 0
                contextBefore = ''
                contextAfter = verseContent
                OccurrenceNote = f'<bold><italics>{GLQuote} </italics></bold>{OccurrenceNote}'
                xmlOutput.append(f"<SelectedText />")
                
            
            xmlOutput.append(f"<StartPosition>{quoteStart}</StartPosition>")
            xmlOutput.append(f"<ContextBefore>{contextBefore}</ContextBefore>")
            xmlOutput.append(f"<ContextAfter>{contextAfter.rstrip()}</ContextAfter>")

        xmlOutput.append("<Status></Status>")
        xmlOutput.append("<Type></Type>")
        xmlOutput.append("<ConflictType />")
        xmlOutput.append(f"<Verse>{verseContent}</Verse>")
        xmlOutput.append("<AssignedUser>unfoldingWord</AssignedUser>")
        xmlOutput.append("<ReplyToUser />")
        xmlOutput.append("<HideInTextWindow>true</HideInTextWindow>")
        xmlOutput.append(f'<Contents>{OccurrenceNote.rstrip()}</Contents>')
        xmlOutput.append("<TagAdded>2</TagAdded>")
        xmlOutput.append("<TagRemoved>1</TagRemoved>")
        xmlOutput.append('</Comment>')


    with open("C:/My Paratext 9 Projects/ULT/Notes_Benjamin Wright.xml", mode='a', encoding='utf8') as notesFile:
        for item in xmlOutput:
            notesFile.write(item + '\n')
    #     notesFile.write("</CommentList>")
    # bookworked = input("Try book, did it work?")
    # if bookworked.lower == 'n':
    #     brokenbooks.append(bookLoc[3:6]) 
    # elif bookworked == 'q': break
    # with open("C:/My Paratext 9 Projects/ULT/Notes_Benjamin Wright.xml",  encoding='utf8') as notesFile:
    #     a = notesFile.readlines()
    #     a.pop(-1)
    # with open("C:/My Paratext 9 Projects/ULT/Notes_Benjamin Wright.xml", mode='w', encoding='utf8') as notesFile:
    #     notesFile.writelines(a)

# print(brokenbooks)

with open("C:/My Paratext 9 Projects/ULT/Notes_Benjamin Wright.xml", mode='a', encoding='utf8') as notesFile:
    notesFile.write("</CommentList>")