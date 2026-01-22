from datetime import datetime
from email.quoprimime import quote
from operator import contains
import re, glob
import html


brokenbooks = []

TNfilesLocation = "./spanish/*.tsv"
ULTfilesLocation = "./spanish/"
TAfilesLocation = "C:/Users/benja/Documents/GitHub/es-419_ta/translate/"


now = datetime.now().strftime("%Y-%m-%dT%H:%M:%S")
opener = [
    '<?xml version="1.0" encoding="utf-8"?>',
    '<CommentList>',
    f'<Comment Thread="LicenseInfo" User="Perry Oakes" VerseRef="RUT 1:0" Language="spa-419" Date="{now}">',
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

with open("C:/My Paratext 9 Projects/SGL/Notes_Perry Oakes.xml", mode='w', encoding='utf8') as notesFile:
     for line in opener:
        notesFile.write(f'{line}\n')

booksToCheck = [
    "GEN",
    "EXO",
    "LEV",
     "NUM",
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
    # Extract book code: remove .tsv extension, take last 3 chars
    Book = TNfile.replace('.tsv', '')[-3:]
    print(Book)
    if Book not in booksToCheck: continue

    # Find matching USFM file (e.g., *rut.usfm)
    usfmFiles = glob.glob(f"{ULTfilesLocation}glt/*{Book.lower()}.usfm")
    if len(usfmFiles) == 0:
        print(f"No USFM file found for {Book}")
        continue
    usfmFile = usfmFiles[0]

    with open(TNfile, encoding = 'utf8')as tnFile:
        tnFile.readline()
        tNotes = tnFile.readlines()
    with open(usfmFile, encoding='utf8') as scriptureFile:
        scriptureBook = scriptureFile.readlines()

    for note in tNotes:
        now = datetime.now().strftime("%Y-%m-%dT%H:%M:%S.%f")
        parts = note.split('\t')
        if len(parts) != 9:
            print(f"Skipping line with {len(parts)} columns: {note[:50]}")
            continue
        # New format: Reference, ID, Tags, SupportReference, Quote, Occurrence, GLQuote, GLOccurrence, Note
        Reference, tcID, Tags, SupportReference, OrigQuote, Occurrence, GLQuote, GLOccurrence, OccurrenceNote = note.split('\t')

        # Split Reference to get Chapter and Verse (format: "chapter:verse" or "front:intro")
        if ':' in Reference:
            Chapter, Verse = Reference.split(':', 1)
        else:
            Chapter = Reference
            Verse = '0'

        # Process OccurrenceNote: first escape HTML, then add markup
        OccurrenceNote = html.escape(OccurrenceNote, quote=False)
        OccurrenceNote = OccurrenceNote.replace('<br><br>', '<br />')
        OccurrenceNote = OccurrenceNote.replace('<br>', '<br />')
        OccurrenceNote = re.sub(r'\*\*(.*?)\*\*', r'<bold>\1</bold>', OccurrenceNote)
        # Match TA articles with either rc://en/ta/... or rc://*/ta/...
        taArticle = re.findall(r'\[\[rc:\/\/(?:\*|en)\/ta\/man\/translate\/(.*?)]]', OccurrenceNote)
        if len(taArticle) > 0:
            taArticle = taArticle[0]
            taArticleTitle = ''
            try:
                with open(TAfilesLocation + taArticle + "/title.md", encoding = 'utf8') as taTitle:
                    taArticleTitle = html.escape(taTitle.readline(), quote=False)
            except: taArticleTitle = html.escape(taArticle, quote=False)
            OccurrenceNote = re.sub(r'\[\[rc:\/\/(?:\*|en)\/ta\/man\/translate\/(.*?)]]', taArticleTitle + r' at https://preview.door43.org/u/es-419_gl/es-419_ta/master#translate--\1', OccurrenceNote)
        if Chapter == 'front' : Chapter = '1'
        if  Verse == 'intro': Verse = '0'
        if Chapter != '0' and Verse != '0':
            chapterStart = scriptureBook.index(f'\\c {Chapter}\n')
            verseLocation = chapterStart + 1
            foundVerse = False
            while not foundVerse and verseLocation < len(scriptureBook):
                if scriptureBook[verseLocation].startswith(f'\\v {Verse} '): 
                    foundVerse = True
                else: verseLocation += 1
            verseContent = scriptureBook[verseLocation].split(' ', 2)[2]
            # removes bracketing or usfm \add tags
            verseContent.replace('{','')
            verseContent.replace('}','')
            verseContent.replace('\\add*','')
            verseContent.replace('\\add ','')

        else: verseContent = ''

        # Escape XML special characters for fields not yet escaped
        tcID_esc = html.escape(tcID, quote=True)
        verseContent_esc = html.escape(verseContent, quote=False)
        GLQuote_esc = html.escape(GLQuote, quote=False)
        # OccurrenceNote is already escaped and has markup added

        xmlOutput.append(f'<Comment Thread="{tcID_esc}" User="unfoldingWord" VerseRef="{Book} {Chapter}:{Verse}" Language="en-US" Date="{now}">')
        if len(GLQuote) == 0:
            xmlOutput.append("<SelectedText />")
            xmlOutput.append("<StartPosition>0</StartPosition>")
            xmlOutput.append("<ContextBefore></ContextBefore>")
            xmlOutput.append(f"<ContextAfter>{verseContent_esc}</ContextAfter>")
        else:
            if contains(verseContent, GLQuote):
                quoteStart = verseContent.index(GLQuote)
                quoteFinish = quoteStart + len(GLQuote) + 1
                contextBefore = html.escape(verseContent[:quoteStart], quote=False)
                contextAfter = html.escape(verseContent[quoteFinish:], quote=False)
                xmlOutput.append(f"<SelectedText> {GLQuote_esc} </SelectedText>")
            else:
                quoteStart = 0
                contextBefore = ''
                contextAfter = verseContent_esc
                OccurrenceNote = f'<bold><italics>{GLQuote_esc} </italics></bold>{OccurrenceNote}'
                xmlOutput.append(f"<SelectedText />")


            xmlOutput.append(f"<StartPosition>{quoteStart}</StartPosition>")
            xmlOutput.append(f"<ContextBefore>{contextBefore}</ContextBefore>")
            xmlOutput.append(f"<ContextAfter>{contextAfter.rstrip()}</ContextAfter>")

        xmlOutput.append("<Status></Status>")
        xmlOutput.append("<Type></Type>")
        xmlOutput.append("<ConflictType />")
        xmlOutput.append(f"<Verse>{verseContent_esc}</Verse>")
        xmlOutput.append("<AssignedUser>unfoldingWord</AssignedUser>")
        xmlOutput.append("<ReplyToUser />")
        xmlOutput.append("<HideInTextWindow>true</HideInTextWindow>")
        xmlOutput.append(f'<Contents>{OccurrenceNote.rstrip()}</Contents>')
        xmlOutput.append("<TagAdded>2</TagAdded>")
        xmlOutput.append("<TagRemoved>1</TagRemoved>")
        xmlOutput.append('</Comment>')

    with open("C:/My Paratext 9 Projects/SGL/Notes_Perry Oakes.xml", mode='a', encoding='utf8') as notesFile:
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

with open("C:/My Paratext 9 Projects/SGL/Notes_Perry Oakes.xml", mode='a', encoding='utf8') as notesFile:
    notesFile.write("</CommentList>")