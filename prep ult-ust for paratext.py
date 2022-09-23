
from glob import glob

ULTfilesLocation = "C:/Users/benja/Downloads/ult/*.usfm"
USTfilesLocation = "C:/Users/benja/Downloads/ust/*.usfm"

def changebracketsToAdd(filesLocation):
    for usfmFile in glob(filesLocation):
        old = []
        with open(usfmFile, encoding = 'utf8') as read:
            old = read.readlines()
        with open(usfmFile, 'w', encoding = 'utf8') as write:        
            for line in old:
                newline = line.replace('{',r'\add ')
                newline = newline.replace('}',r'\add*')
                newline = newline.replace(r'\add* \add ',' ')
                write.write(newline)

changebracketsToAdd(ULTfilesLocation)
changebracketsToAdd(USTfilesLocation)

