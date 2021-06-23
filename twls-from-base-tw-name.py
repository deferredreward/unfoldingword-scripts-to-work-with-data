import io

# CHANGE THIS to the path to your TWL file, it might be in your downloads directory
filename = "C:/Users/benja/Google Drive/scripting/twl_EXO - sample.tsv"

twbaselink = "rc://*/tw/dict/bible"

with io.open("twlinksindex.txt", encoding='utf8') as f:
    twlinkslist = f.readlines()

with io.open(filename, encoding='utf8') as f:
    with io.open(filename.replace('.tsv','-new.tsv'), 'w', encoding='utf8', newline='\n') as newFile:
        for line in f:

            ls = line.split('\t')
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
            elif "/names/" in ls[5]:
                ls[2] = "name"
            elif "/other/" in ls[5]:
                ls[2] = ""                          
            ls[5] = ls[5].replace("\\*","*")
            newLine = "\t".join(ls)
            newFile.write(newLine)
