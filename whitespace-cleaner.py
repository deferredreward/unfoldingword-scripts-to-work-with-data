import io, os

# CHANGE THIS to the path to your TN file, it might be in your downloads directory
filename = "C:/Users/benja/Documents/GitHub/en_tn/en_tn_02-EXO.tsv"
os.rename(filename,filename.replace('.tsv','.old'))
filename = filename.replace('.tsv','.old')

with io.open(filename, encoding='utf8') as f:
    with io.open(filename.replace('.old','.tsv'), 'w', encoding='utf8', newline='\n') as newFile:
        for line in f:
            newLine = line.replace('\u200c', '').replace('\u200b', '').replace('\u00A0', '')
            ls = newLine.split('\t')
            tab = 0
            while tab < len(ls):
                ls[tab] = ls[tab].strip()
                ls[tab] = ls[tab].strip('\u2060')
                tab += 1
            newLine = "\t".join(ls) + '\n'
            newFile.write(newLine)