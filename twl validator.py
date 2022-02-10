import io, os, glob, random
pathTWL= "C://Users//benja//Documents//uwgit//en_twl//"
idList = []


with io.open("twlinksindex.txt", encoding='utf8') as f:
    twlinkslist = f.readlines()

def makeNewID(oldID):
    abcs = "qwertyuioplkjhgfdsazxcvbnm" # quicker to type
    numbers = "1234567890"
    newID = ""
    isNotUniqueID = 1
    while isNotUniqueID != 0:
        newID = random.choice(abcs) + random.choice(abcs + numbers) + random.choice(abcs + numbers) + random.choice(abcs + numbers)
        isNotUniqueID = idList.count(newID)
        idList.pop(oldID)
        idList.append(newID)        
    return newID

def validateLink(line):

    ls = line.split('\t')
    # ls[5] is the TWLink field
    # ls[2] is the tag field
    if '\n' not in ls[5]: ls[5] += '\n'
    if twbaselink + "/kt/" + ls[5] in twlinkslist:
        ls[2] = "keyterm"
        ls[5] = twbaselink + "/kt/" + ls[5]
    elif twbaselink + "/names/" + ls[5] in twlinkslist:
        ls[2] = "name"
        ls[5] = twbaselink + "/names/" + ls[5]
    elif twbaselink + "/other/" + ls[5] in twlinkslist:
        ls[2] = ""
        ls[5] = twbaselink + "/other/" + ls[5]      
    elif "/kt/" in ls[5]:
        ls[2] = "keyterm"
        if "jesus" in ls[5]:
            ls[2] += "; name"        
    elif "/names/" in ls[5]:
        ls[2] = "name"
    elif "/other/" in ls[5]:
        ls[2] = ""                          
    ls[5] = ls[5].replace("\\*","*")

    if ls[1][0].isdigit():
        ls[1] = makeNewID(ls[1])  # the function is written as if this is passing in a list

    return "\t".join(ls)

print("ran to here")
for filename in glob.glob(os.path.join(pathTWL, '*.tsv')):
    # print("but not here")
    # print(filename)
    # CHANGE THIS to the path to your TWL file, it might be in your downloads directory
    # filename = "C:/Users/benja/Documents/uwgit/en_twl/twl_EXO.tsv"
    os.rename(filename,filename.replace('.tsv','.old'))
    filename = filename.replace('.tsv','.old')
    twbaselink = "rc://*/tw/dict/bible"

with io.open(filename, encoding='utf8') as f:
    for line in f:
        idList.append(line.split('\t')[1])


    with io.open(filename, encoding='utf8') as f:
        with io.open(filename.replace('.old','.tsv'), 'w', encoding='utf8', newline='\n') as newFile:
            for line in f:
                newFile.write(validateLink(line))

                # ls = line.split('\t')
                # # ls[5] is the TWLink field
                # # ls[2] is the tag field
                # if '\n' not in ls[5]: ls[5] += '\n'
                # if twbaselink + "/kt/" + ls[5] in twlinkslist:
                #     ls[2] = "keyterm"
                #     ls[5] = twbaselink + "/kt/" + ls[5]
                # elif twbaselink + "/names/" + ls[5] in twlinkslist:
                #     ls[2] = "name"
                #     ls[5] = twbaselink + "/names/" + ls[5]
                # elif twbaselink + "/other/" + ls[5] in twlinkslist:
                #     ls[2] = ""
                #     ls[5] = twbaselink + "/other/" + ls[5]      
                # elif "/kt/" in ls[5]:
                #     ls[2] = "keyterm"
                # elif "/names/" in ls[5]:
                #     ls[2] = "name"
                # elif "/other/" in ls[5]:
                #     ls[2] = ""                          
                # ls[5] = ls[5].replace("\\*","*")
                # newLine = "\t".join(ls)
                # newFile.write(newLine)
print("and here")