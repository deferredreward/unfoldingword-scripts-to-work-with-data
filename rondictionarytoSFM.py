
RonDictionary = "./RonDictionary.txt"
newRonDictionary = './newRonDict.db'
problemFile = "./problemLines.txt"
problemList = []

with open(RonDictionary, encoding="utf8") as RD:
    with open(newRonDictionary, 'w', encoding="utf8", ) as nRD:
        with open(problemFile, 'w', encoding="utf8") as pf:
            for line in RD:
                if "-" in line:
                    word, pregloss = line.split("-", 1)
                    word = word.strip()
                    pregloss = pregloss.strip()
                    if "/" in word or "\\" in word or " see " in word:
                        pf.write(line)
                        continue # I don't want to further process this line
                    if pregloss.startswith('n ') or pregloss.startswith('v ') or pregloss.startswith('adj ') or pregloss.startswith('adv ') or pregloss.startswith('q '):
                        partofSpeech, gloss = pregloss.split(" ", 1)
                        nRD.write("\lx " + word + "\n")
                        nRD.write("\ps " + partofSpeech + "\n")
                        nRD.write("\ge " + gloss + '\n')
                    else:
                        pf.write(line)
                        continue


                


