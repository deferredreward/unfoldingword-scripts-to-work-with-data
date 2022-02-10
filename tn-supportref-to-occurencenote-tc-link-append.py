import io, os, random
idList = []

def makeNewID(oldID):
    abcs = "qwertyuioplkjhgfdsazxcvbnm" # quicker to type
    numbers = "1234567890"
    newID = ""
    isNotUniqueID = 1
    while isNotUniqueID != 0:
        newID = random.choice(abcs) + random.choice(abcs + numbers) + random.choice(abcs + numbers) + random.choice(abcs + numbers)
        isNotUniqueID = idList.count(newID)
        print( "=>" + newID)
        idList.pop(oldID)
        idList.append(newID)
    return newID

# CHANGE THIS to the path to your TN file, it might be in your downloads directory
filename = "C:/Users/benja/Documents/uwgit/en_tn/en_tn_02-EXO.tsv"
os.rename(filename,filename.replace('.tsv','.old'))
filename = filename.replace('.tsv','.old')

with io.open(filename, encoding='utf8') as f:
    for line in f:
        idList.append(line.split('\t')[1])

with io.open(filename, encoding='utf8') as f:
    with io.open(filename.replace('.old','.tsv'), 'w', encoding='utf8', newline='\n') as newFile:
        for line in f:
            newLine = line.replace('\u200c', '').replace('\u200b', '').replace('\u00A0', '')
            ls = newLine.split('\t')
            if "-" in ls[4] and "[[rc:" not in ls[8]:
                newOcNo = ls[8].rstrip() + " (See: [[rc://en/ta/man/translate/" + ls[4].strip() + "]])\n"
                ls[8] = newOcNo
            tab = 0
            while tab < len(ls):
                ls[tab] = ls[tab].strip()
                ls[tab] = ls[tab].strip('\u2060')
                tab += 1
            if ls[3][0].isdigit():
                ls[3] = makeNewID(ls[3])
            newLine = "\t".join(ls) + '\n'
            newFile.write(newLine)
