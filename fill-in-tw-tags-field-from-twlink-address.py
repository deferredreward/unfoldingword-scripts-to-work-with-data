import io

# CHANGE THIS to the path to your TWL file, it might be in your downloads directory
filename = "C:/Users/benja/Google Drive/scripting/twl_EXO.tsv"

with io.open(filename, encoding='utf8') as f:
    with io.open(filename.replace('.tsv','-new.tsv'), 'w', encoding='utf8', newline='\n') as newFile:
        for line in f:
            ls = line.split('\t')
            if "/kt/" in ls[5]:
                ls[2] = "keyterm"
            elif "/names/" in ls[5]:
                ls[2] = "name"
            elif "/other/" in ls[5]:
                ls[2] = ""
            ls[5] = ls[5].replace("\\*","*")
            newLine = "\t".join(ls)
            newFile.write(newLine)
