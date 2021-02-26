import re, io, os

# edit these:
filename = "./02-EXO.usfm"
tupleOfLines = (2461,2601,2756,2771,3368,6680,6749,2576,2667,2585,2646,12628,3179,3459,5529,7040,7822,7855,12139,12144,12151,12167,13385,15731,15816,3341,3372,3452,3470,3521,3533,7489,7494,7535,7812,7815,11207,12963,12988,12975,12979,12982,14639,4264,6426,6538,6566,6578,4412,4486,12625,5365,5479,6370,6771,11717,14385,5379,5765,5647,12931,5838,13800,5889,8237,5892,5920,5959,7363,9228,9615,9683,9701,10378,10393,10724,12057,12061,12322,12432,12535,12687,12937,12976,12980,12983,14011,15734,16362,16495,16517,16684,16705,6296,6483,9362,6951,9221,7441,8063,8104,8111,8635,12618,12645,9783,13677)

# end edit these


twLink =  re.compile(r' x-tw=\".*?\"')


lineNumber = 1
with io.open(filename, encoding='utf8') as f:
    with io.open(filename.replace('.usfm','-new.usfm'), 'w', encoding='utf8', newline='\n') as newFile:
        for line in f:
            if lineNumber in tupleOfLines:
                line = re.sub(twLink, '', line)
                #print("found on line " + str(lineNumber))
            newFile.write(line)
            lineNumber+=1
