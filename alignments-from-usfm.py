import os, glob, re, sys, datetime

ignoreList = ["the", "a", "an", "and", "or", "but", "of", "to", "at", "from", "in", "his", "my", "according", "for", "by", "your", "toward", "is", "who", "that", "which", "he", "they", "them", "so", "him", "her", "this", "that", "she", "you", "as", "on", "are", "me", "it", "its", "have", "then", "be", "I", "than", "had", "their", "s", "o", 'we', 'has', 'been', 'being']

filesLocation = "C:/Users/benja/Documents/GitHub/en_ult/*.usfm"

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




strongs = input("Enter strong # to check alignments: ").upper()
print()

possibleTranslations = {}
print("checking: " ,end = '')
for filename in glob.glob(filesLocation):
    if filename[-11] == "A": continue
    if filename[-8:-5] not in booksToCheck: continue
    if strongs[0] == "H" and int(filename[-11]) > 4: continue
    elif strongs[0] == "G" and int(filename[-11]) < 4: continue
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
                    #print(location, end = ' ')
                    for translation in alignedWords:                        
                        if len(translation) == 0: continue
                        translationLower = translation.lower()
                        if translationLower in ignoreList: continue
                        if translationLower not in possibleTranslations: 
                                possibleTranslations.update({translationLower:[location]})
                                #print(translation, end=' ')
                        elif translationLower in possibleTranslations:
                                possibleTranslations[translationLower].append(location)
                    #print()
            except: pass

now = datetime.datetime.now().strftime("%Y-%m-%d %H.%M")
resultFile = strongs + "_results at " + now + ".txt"
with open(os.path.join(sys.path[0], resultFile), "w") as f:
    f.write("Strongs#: " + strongs + '\n')
    #sorted_items = sorted(possibleTranslations.items(),  key = lambda item : len(item[1]))
    sorted_items = {key: value for key, value in sorted(possibleTranslations.items())}
    sortedPossibleTranslations = dict(sorted_items)
    for item in sortedPossibleTranslations.keys():
        f.write('\n')        
        f.write(item.upper() + " : " + str(len(sortedPossibleTranslations[item])) + 'x in: ')
        for values in sortedPossibleTranslations[item]:
            f.write(values.upper())
            f.write(', ')
print('\n' + str(os.path.join(sys.path[0], resultFile)) + " written.")