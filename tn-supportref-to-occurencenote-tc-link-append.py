import io, os

# CHANGE THIS to the path to your TN file, it might be in your downloads directory
filename = "C:/Users/benja/Documents/uwgit/en_tn/en_tn_02-EXO.tsv"
os.rename(filename,filename.replace('.tsv','.old'))
filename = filename.replace('.tsv','.old')

with io.open(filename, encoding='utf8') as f:
    with io.open(filename.replace('.old','.tsv'), 'w', encoding='utf8', newline='\n') as newFile:
        for line in f:
            ls = line.split('\t')
            if "-" in ls[4] and "[[rc:" not in ls[8]:
                newOcNo = ls[8].rstrip() + " (See: [[rc://en/ta/man/translate/" + ls[4].strip() + "]])\n"
                ls[8] = newOcNo
            newLine = "\t".join(ls)
            newFile.write(newLine)
