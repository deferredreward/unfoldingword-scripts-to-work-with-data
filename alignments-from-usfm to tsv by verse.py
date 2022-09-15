import os, glob, re, sys, datetime, time

ULTfilesLocation = "C:/Users/benja/Documents/uwgit/en_ult/*.usfm"
USTfilesLocation = "C:/Users/benja/Documents/uwgit/en_ust/*.usfm"

def findStrongsAlignments(filesLocation):

    ignoreList = ["the", "a", "an", "and", "or", "but", "of", "to", "at", "from", "in", "his", "my", "according", "for", "by", "your", "toward", "is", "who", "that", "which", "he", "they", "them", "so", "him", "her", "this", "that", "she", "you", "as", "on", "are", "me", "it", "its", "have", "then", "be", "I", "than", "had", "their", "s", "o", 'we', 'has', 'been', 'being']

    booksToCheck = [
        "GEN",
        "EXO",
        "LEV",
        "NUM",
        "DEU",
        "JOS",
        "JDG",
        "RUT",
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

    reChapter  = re.compile(r".*\\{1,2}c\s(\d{1,3})")
    reVerse = re.compile(r".*\\{1,2}v\s(\d{1,3})")
    reStrongs = re.compile(r'x-strong="([HG]\d{4,5})')
    reWords = re.compile(r'\\w (\w+)|')

    currentBook = ''
    currentChapter = ''
    currentVerse = ''
    alignedWords = []

    possibleTranslations = {}
    print("checking: " ,end = '')
    for filename in glob.glob(filesLocation):
        if filename[-11] == "A": continue
        if filename[-8:-5] not in booksToCheck: continue
        if strongs[0].upper() == "H" and int(filename[-11]) > 4: continue
        elif strongs[0].upper() == "G" and int(filename[-11]) < 4: continue
        currentBook = ''
        currentChapter = ''
        currentVerse = ''
        alignedWords = []
        with open(os.path.join(os.getcwd(), filename), 'r', encoding='utf8') as f:
            book = f.read().replace('\n',' ')
            booklines = book.split('\zaln-e\*')
            currentBook = booklines[0][4:7]
            print(currentBook + "…", end = '')
            for line in booklines:
                oldChapter = currentChapter
                oldVerse = currentVerse
                try:                 
                    currentChapter = re.search(reChapter, line).group(1)
                except: 
                    currentChapter = oldChapter
                try:                
                    currentVerse = re.search(reVerse, line).group(1)
                except: 
                    currentVerse = oldVerse
                try:
                    if re.search(strongs, line):
                        alignedWords = re.findall(reWords, line)
                        location = currentBook + " " + currentChapter + ":" + currentVerse
                        for translation in alignedWords:                        
                            if len(translation) == 0: continue
                            translationLower = translation.lower()
                            if translationLower in ignoreList: continue
                            if translationLower not in possibleTranslations: 
                                    possibleTranslations.update({translationLower:[location]})
                            elif translationLower in possibleTranslations:
                                    possibleTranslations[translationLower].append(location)
                except: pass

    sorted_items = {key: value for key, value in sorted(possibleTranslations.items())}
    sortedPossibleTranslations = dict(sorted_items)
    return sortedPossibleTranslations

def sortByVerse(possibleTranslations):    
    possibleTranslationsByRef = {}
    for k, v in possibleTranslations.items():
        for x in v:
            possibleTranslationsByRef.setdefault(x,[]).append(k)
    sorted_items = {key: value for key, value in sorted(possibleTranslationsByRef.items())}
    sortedPossibleTranslations = dict(sorted_items)
    return sortedPossibleTranslations
    
def makeResultByWordFile(file, possibleTranslations):        
    for key in possibleTranslations.keys():
        f.write('\n')        
        f.write(key.lower() + " : " + str(len(possibleTranslations[key])) + 'x in: ')
        for values in possibleTranslations[key]:
            f.write(values.lower())
            f.write(', ')


# Main

strongs = input("Enter strong # to check alignments: ").upper()
start_time = time.time()
print('\nULT ')
ULTpossibletranslations = findStrongsAlignments(ULTfilesLocation)
print('\nUST ')
USTpossibletranslations =  findStrongsAlignments(USTfilesLocation)

ULTptSortedbyVerse = sortByVerse(ULTpossibletranslations)
USTptSortedbyVerse = sortByVerse(USTpossibletranslations)

topWord = ''
x= 0
for k, v in ULTpossibletranslations.items():
    if len(v) > x:
        x = len(v)
        topWord = k.lower()

now = datetime.datetime.now().strftime("%Y-%m-%d %H.%M")
resultFileByRef = f"{strongs}={topWord}_result sorted by verse at {now}.tsv"
resultFileByWord = f"{strongs}={topWord}_result sorted by ULT rendering at {now}.txt"

with open(os.path.join(sys.path[0], resultFileByRef), "w") as f:
    f.write("Reference\tULT\tUST")
    for key in ULTptSortedbyVerse.keys():
        f.write('\n')        
        f.write(f'{key}\t')
        for value in ULTptSortedbyVerse[key]:
            f.write(value.lower())
            if len(ULTpossibletranslations[value]) > 1:
                f.write(f' {str(len(ULTpossibletranslations[value]))}x')
            f.write(', ')
        f.write('\t')
        if key in USTptSortedbyVerse:
            for value in USTptSortedbyVerse[key]:
                f.write(value.lower())
                if len(USTpossibletranslations[value]) > 1:
                    f.write(f' {str(len(USTpossibletranslations[value]))}x')
                f.write(', ')
    print('\n' + str(os.path.join(sys.path[0], resultFileByRef)) + " written.\n")

with open(os.path.join(sys.path[0], resultFileByWord), "w") as f:
    f.write("Strongs#: " + strongs + '\n')
    f.write('ULT:\n')
    makeResultByWordFile(f, ULTpossibletranslations)
    f.write('\n\nUST:\n')
    makeResultByWordFile(f, USTpossibletranslations)
    print('\n' + str(os.path.join(sys.path[0], resultFileByRef)) + " written.\n")

duration = time.time() - start_time
print(f"Duration {duration} seconds")