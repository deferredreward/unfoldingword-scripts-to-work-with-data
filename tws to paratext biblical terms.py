
from operator import contains
from pathlib import Path
import glob, multiprocessing, os

TWL_Location = 'C:/Users/benja/Documents/GitHub/en_twl/*.tsv'
TW_Location = 'C:/Users/benja/Documents/GitHub/en_tw/bible/'
output_Location = 'C:/Users/benja/Documents/GitHub/scriptoutput/'

def createTWLtoBibleReferenceKey(fileLocation):
    thisBookTWsAreAt = {}
    book = fileLocation[-7:-4]
    with open(os.path.join(os.getcwd(), fileLocation), encoding='utf8') as f:
        f.readline()        
        for line in f:
            chapVerse = line.split('\t', 1)[0]
            article = line.split('\t')[-1].split('/')[-1].rstrip()
            if article not in thisBookTWsAreAt:
                thisBookTWsAreAt.update({article:[f'{book} {chapVerse}']})
            else:
                thisBookTWsAreAt[article].append(f'{book} {chapVerse}')

    return thisBookTWsAreAt

def makeOneDictSortedByABC(wordLocationsByBookL):
    allWordLocationsL = {}
    for nextDictionary in wordLocationsByBookL:         
        if nextDictionary != None:   
            for key, value in nextDictionary.items():
                if key in allWordLocationsL:
                    allWordLocationsL[key].extend(value)
                else:
                    allWordLocationsL[key] = value
    return dict({key: value for key, value in sorted(allWordLocationsL.items())})

def makeBiblicalTermsandRenderings(allWordLocationsL):
        with open(os.path.join(output_Location, "ProjectBiblicalTerms.xml"), "w", encoding='utf8') as bt:
            bt.write('<?xml version="1.0" encoding="utf-8"?>\n\t<BiblicalTermsList>\n')
            with open(os.path.join(output_Location, "TermRenderings.xml"), "w", encoding='utf8') as tr:                
                tr.write('<?xml version="1.0" encoding="utf-8"?>\n\t<TermRenderingsList>\n')

                # How to access subdirectory files 
                # https://stackoverflow.com/questions/2186525/how-to-use-glob-to-find-files-recursively
                for path in Path(TW_Location).rglob('*.md'):
                    article = path.name.split('.')[0]
                    if  contains(str(path), 'name'):
                        article = article.capitalize()
                        
                    if allWordLocationsL.get(article.lower()) != None:
                        with open(path, encoding='utf8') as twa: 
                            bt.write(f'\t\t<Term Id="{article}">\n')     
                            headerline = twa.readline().replace('# ', '')
                            bt.write(f'\t\t\t<Gloss>{headerline}</Gloss>\n')
                            bt.write('\t\t\t<References>\n')
                            for value in allWordLocationsL[article.lower()]:
                                bt.write(f'\t\t\t\t<Verse>{value}</Verse>\n')
                            bt.write('\t\t\t</References>\n')
                            bt.write('\t\t</Term>')

                            tr.write(f'\t<TermRendering Id="{article}" Guess="false">\n\t\t<Notes>\n')
                            for line in twa:
                                tr.write(f'{line}&lt;br&gt;\n')
                            tr.write('\t\t</Notes>\n')
                            tr.write('\t</TermRendering>\n')

                tr.write('</TermRenderingsList>')
            bt.write('\t<Versification>English</Versification>\n</BiblicalTermsList>')
  


if __name__ == "__main__":
    wordLocationsByBook = []
    with multiprocessing.Pool() as pool:
        wordLocationsByBook = pool.map(createTWLtoBibleReferenceKey, glob.glob(TWL_Location))
    allWordLocations = makeOneDictSortedByABC(wordLocationsByBook)
    makeBiblicalTermsandRenderings(allWordLocations)






    # kicks out a tsv for checking or anything else we might want
    with open(os.path.join(output_Location, "twArticlesWithReferences.tsv"), "w") as f:
        for key in allWordLocations.keys():
            f.write(f'{key}\t')
            for value in allWordLocations[key]:
                f.write(f"{value}, ")
            f.write('\n')
    