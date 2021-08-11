import io, json

ignoreList = ["the", "a", "an", "and", "or", "but", "of", "to", "at", "from", "in", "his", "my", "according", "for", "by", "your"]

tCoreProjectsDir = "C:/Users/benja/translationCore/projects/"
projects = ["jon" , "exo", "est",  "neh", "oba", "rut"]  # finished (or mostly) BPs

ultPrefix = "en_ult_"
ustPrefix = 'en_ust_'
bookPostfix = '_book'

pathToAlignment = "/.apps/translationCore/alignmentData/"

strongs = input("Enter strong #: ").upper()

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
        except: continue
    if prefix == ultPrefix: print("ULT:")
    else: print("UST:")
    for item in possibleTranslations.keys():
        print("-------------------------------------")
        print(item + " : " + str(len(possibleTranslations[item])) + 'x in: ' + str(possibleTranslations[item]))
    print("-------------------------------------")

findTranslations(ustPrefix)
findTranslations(ultPrefix)

"""
figuring out json structure
print(content["1"]["alignments"][0]["topWords"][0]["strong"])
print(content["1"]["alignments"][0]["bottomWords"][1]["word"])
print(len(content["1"]["alignments"][0]["bottomWords"]))

"""