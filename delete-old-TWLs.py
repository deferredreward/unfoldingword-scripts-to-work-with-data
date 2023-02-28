
from glob import glob

TWLfilesLocation = "C:/Users/benja/Documents/uwgit/en_twl/*.tsv"
DeleteList = "C:/Users/benja/Documents/uwgit/unfoldingword-scripts-to-work-with-data/twltodelete.txt"
toDelete = []

with open(DeleteList) as read:
    for line in read:
        toDelete.append(line.lower())
# print(toDelete)
# x = 0
# while x < len(toDelete):
#     toDelete[x] = toDelete[x].lower()
#     x += 1

for TWLFile in glob(TWLfilesLocation):
    old = []
    with open(TWLFile, encoding = 'utf8') as read:
        old = read.readlines()
    with open(TWLFile, 'w', encoding = 'utf8') as write:        
        for line in old:
            article = line.split("/")[-1]
            if article.lower() in toDelete: continue #print(article)
            else: write.write(line)


