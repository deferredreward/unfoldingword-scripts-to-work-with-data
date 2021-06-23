import io, glob

twbasedir = "C:/Users/benja/Documents/uwgit/en_tw/bible"

kt = "/kt"
names = "/names"
other = "/other"

twbaselink = "rc://*/tw/dict/bible"

listoflinks = []
with io.open("twlinksindex.txt", 'w', encoding='utf8', newline='\n') as newFile:
    for file in glob.glob(twbasedir + '/**/*.md', recursive=True):
        ending = file.split("bible")[1].replace('.md','')        
        newFile.write(twbaselink + ending.replace('\\', '/') + '\n')



