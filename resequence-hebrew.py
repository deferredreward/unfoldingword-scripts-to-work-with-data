import io

# CHANGE THIS to the path to your file, it might be in your downloads directory
filename = "C:/Users/benja/Downloads/05-DEU-master.usfm"
outputfile = "C:/Users/benja/Downloads/05-DEU.usfm"

with io.open(filename, encoding='utf8') as f:
    with io.open(outputfile, 'w', encoding='utf8', newline='\n') as newFile:

        content = f.read()
        # daghesh issues
        # all items are swapping the named item for daghesh as in first
        content = content.replace('\u05B1\u05BC',u'\u05BC\u05B1') # hatheph seghol-daghesh => daghesh-hatheph seghol
        content = content.replace('\u05B2\u05BC',u'\u05BC\u05B2') # hateph pathach
        content = content.replace('\u05B3\u05BC',u'\u05BC\u05B3') # hateph qamets
        content = content.replace('\u05B4\u05BC',u'\u05BC\u05B4') # hireq
        content = content.replace('\u05B5\u05BC',u'\u05BC\u05B5') # tsere
        content = content.replace('\u05B6\u05BC',u'\u05BC\u05B6') # seghol
        content = content.replace('\u05B7\u05BC',u'\u05BC\u05B7') # pathach
        content = content.replace('\u05B8\u05BC',u'\u05BC\u05B8') # qamets
        content = content.replace('\u05B9\u05BC',u'\u05BC\u05B9') # holem
        content = content.replace('\u05BA\u05BC',u'\u05BC\u05BA') # waw holem
        content = content.replace('\u05BB\u05BC',u'\u05BC\u05BB') # qibbuts
        content = content.replace('\u05BD\u05BC',u'\u05BC\u05BD') # meteg
        content = content.replace('\u05B0\u05BC',u'\u05BC\u05B0') # shewa

        # shin dot issues, same sequence as above
        content = content.replace('\u05B1\u05C1',u'\u05C1\u05B1') # hatheph seghol
        content = content.replace('\u05B2\u05C1',u'\u05C1\u05B2') # hateph pathach
        content = content.replace('\u05B3\u05C1',u'\u05C1\u05B3') # hateph qamets
        content = content.replace('\u05B4\u05C1',u'\u05C1\u05B4') # hireq
        content = content.replace('\u05B5\u05C1',u'\u05C1\u05B5') # tsere
        content = content.replace('\u05B6\u05C1',u'\u05C1\u05B6') # seghol
        content = content.replace('\u05B7\u05C1',u'\u05C1\u05B7') # pathach
        content = content.replace('\u05B8\u05C1',u'\u05C1\u05B8') # qamets
        content = content.replace('\u05B9\u05C1',u'\u05C1\u05B9') # holem
        content = content.replace('\u05BA\u05C1',u'\u05C1\u05BA') # waw holem
        content = content.replace('\u05BB\u05C1',u'\u05C1\u05BB') # qibbuts
        content = content.replace('\u05BD\u05C1',u'\u05C1\u05BD') # meteg
        content = content.replace('\u05B0\u05C1',u'\u05C1\u05B0') # shewa-shin => shin-shewa

        # sin dot issues
        content = content.replace('\u05B1\u05C2',u'\u05C2\u05B1') # hatheph seghol
        content = content.replace('\u05B2\u05C2',u'\u05C2\u05B2') # hateph pathach
        content = content.replace('\u05B3\u05C2',u'\u05C2\u05B3') # hateph qamets
        content = content.replace('\u05B4\u05C2',u'\u05C2\u05B4') # hireq
        content = content.replace('\u05B5\u05C2',u'\u05C2\u05B5') # tsere
        content = content.replace('\u05B6\u05C2',u'\u05C2\u05B6') # seghol
        content = content.replace('\u05B7\u05C2',u'\u05C2\u05B7') # pathach
        content = content.replace('\u05B8\u05C2',u'\u05C2\u05B8') # qamets
        content = content.replace('\u05B9\u05C2',u'\u05C2\u05B9') # holem
        content = content.replace('\u05BA\u05C2',u'\u05C2\u05BA') # waw holem
        content = content.replace('\u05BB\u05C2',u'\u05C2\u05BB') # qibbuts
        content = content.replace('\u05BD\u05C2',u'\u05C2\u05BD') # meteg
        content = content.replace('\u05B0\u05C2',u'\u05C2\u05B0') # shewa-sin => sin-shewa

        # swap daghesh for shin, sin dot
        content = content.replace('\u05BC\u05C1',u'\u05C1\u05BC') # shin
        content = content.replace('\u05BC\u05C2',u'\u05C2\u05BC') # sin

        newFile.write(content) 
