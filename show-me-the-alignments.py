import io, json

ignoreList = ["the", "a", "an", "and", "or", "but", "of", "to", "at", "from", "in", "his", "my", "according", "for", "by", "your", "toward", "is", "who", "that", "which", "he", "they", "them", "so", "him", "her", "this", "that", "she", "you", "as", "on", "are", "me", "it", "its", "have", "then", "be", "I", "than", "had", "their"]
tCoreProjectsDir = "C:/Users/benja/translationCore/projects/"
projects = ["exo", "est",  "neh", "jon" , "oba", "rut", "ezr", "luk", "1th", "phm", "jud", "php", "2pe", "jas", "jhn", "col", "1pe", "2ti", "2jn", "tit", "3jn", "eph", "1ti", "1jn" ]  # finished (or mostly) BPs

ultPrefix = "en_ult_"
ustPrefix = 'en_ust_'
bookPostfix = '_book'

pathToAlignment = "/.apps/translationCore/alignmentData/"

strongs = input("Enter strong # to check alignments: ").upper()
print()

def findTranslations(prefix):
    possibleTranslations = {}
# possibleTranslations = {"law": ["exo 23:1", "jon 3:1"], "prophet": ["est 3:4", "neh 1:2"]} etc
    content = ""
    for proj in projects: # ULT
        folderPath = tCoreProjectsDir + prefix + proj + bookPostfix + pathToAlignment + proj + "/"
        chapter = 1
        try:
            while chapter < 151:
                with io.open(folderPath + str(chapter) + '.json' , encoding='utf8') as ch:
                    chapContent = ch.read()
                    if chapContent.find(strongs) != -1:
                    #  print("chapContent.find")
                        content = json.loads(chapContent)
                        # parsing out the json
                        verseNum = 1                    
                        while verseNum < 180:
                            try:
                                if json.dumps(content[str(verseNum)]["alignments"]).find(strongs) != -1:
                                #  print("verse.find")
                                    for alignments in content[str(verseNum)]["alignments"]:   
                                    # print(alignments["topWords"][0])                         
                                        for topWords in alignments["topWords"]:                                
                                            if topWords["strong"].find(strongs) != -1:
                                            #  print("you got it!")
                                            #  print(topWords)
                                                for bottomWords in alignments["bottomWords"]:
                                                    translation =  bottomWords["word"]
                                                    location = proj + " " + str(chapter) + ":" + str(verseNum)
                                                    if translation.lower() not in ignoreList and translation not in possibleTranslations:
                                                        possibleTranslations.update({translation: [location]})
                                                    elif translation in possibleTranslations:
                                                        #verseList = possibleTranslations[translation]
                                                        possibleTranslations[translation].append(location)


                            except: break
                            verseNum += 1

                    chapter += 1
        except: 
            
            continue
    if prefix == ultPrefix: print("ULT:")
    else: print("UST:")
    sorted_items = sorted(possibleTranslations.items(),  key = lambda item : len(item[1]))
    sortedPossibleTranslations = dict(sorted_items)
    for item in sortedPossibleTranslations.keys():
        print("\n\n")
        
        print(item.upper() + " : " + str(len(sortedPossibleTranslations[item])) + 'x in: ' , end='')
        for values in sortedPossibleTranslations[item]:
            print(values.upper(), end=', ')
    if prefix == ultPrefix: print("\n\n^^ULT^^")
    else: print("\n\n^^UST^^")    
    print("\n-------------------------------------\n+++++++++++++++++++++\n-----------------------------\n")

findTranslations(ustPrefix)
findTranslations(ultPrefix)

"""
figuring out json structure
print(content["1"]["alignments"][0]["topWords"][0]["strong"])
print(content["1"]["alignments"][0]["bottomWords"][1]["word"])
print(len(content["1"]["alignments"][0]["bottomWords"]))

"""