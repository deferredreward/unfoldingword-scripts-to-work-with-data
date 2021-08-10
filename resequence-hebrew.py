import io

# CHANGE THIS to the path to your  file, it might be in your downloads directory
filename = "C:/Users/benja/Downloads/05-DEU-master.usfm"
outputfile = "C:/Users/benja/Downloads/05-DEU.usfm"

with io.open(filename, encoding='utf8') as f:
    with io.open(outputfile, 'w', encoding='utf8', newline='\n') as newFile:
        print("i'm running")
        # for line in f:
        line = f.read()
        # daghesh issues
        line = line.replace('\u05B0\u05BC','\u05BC\u05B0')
        line = line.replace('\u05B1\u05BC',u'\u05BC\u05B1')
        line = line.replace('\u05B2\u05BC',u'\u05BC\u05B2')
        line = line.replace('\u05B3\u05BC',u'\u05BC\u05B3')
        line = line.replace('\u05B4\u05BC',u'\u05BC\u05B4')
        line = line.replace('\u05B5\u05BC',u'\u05BC\u05B5')
        line = line.replace('\u05B6\u05BC',u'\u05BC\u05B6')
        line = line.replace('\u05B7\u05BC',u'\u05BC\u05B7')
        line = line.replace('\u05B8\u05BC',u'\u05BC\u05B8')
        line = line.replace('\u05B9\u05BC',u'\u05BC\u05B9')
        line = line.replace('\u05BA\u05BC',u'\u05BC\u05BA')
        line = line.replace('\u05BB\u05BC',u'\u05BC\u05BB')
        # shin dot issues
        line = line.replace('\u05B0\u05C1',u'\u05C1\u05B0')
        line = line.replace('\u05B1\u05C1',u'\u05C1\u05B1')
        line = line.replace('\u05B2\u05C1',u'\u05C1\u05B2')
        line = line.replace('\u05B3\u05C1',u'\u05C1\u05B3')
        line = line.replace('\u05B4\u05C1',u'\u05C1\u05B4')
        line = line.replace('\u05B5\u05C1',u'\u05C1\u05B5')
        line = line.replace('\u05B6\u05C1',u'\u05C1\u05B6')
        line = line.replace('\u05B7\u05C1',u'\u05C1\u05B7')
        line = line.replace('\u05B8\u05C1',u'\u05C1\u05B8')
        line = line.replace('\u05B9\u05C1',u'\u05C1\u05B9')
        line = line.replace('\u05BA\u05C1',u'\u05C1\u05BA')
        line = line.replace('\u05BB\u05C1',u'\u05C1\u05BB')
        # sin dot issues
        line = line.replace('\u05B0\u05C2',u'\u05C2\u05B0')
        line = line.replace('\u05B1\u05C2',u'\u05C2\u05B1')
        line = line.replace('\u05B2\u05C2',u'\u05C2\u05B2')
        line = line.replace('\u05B3\u05C2',u'\u05C2\u05B3')
        line = line.replace('\u05B4\u05C2',u'\u05C2\u05B4')
        line = line.replace('\u05B5\u05C2',u'\u05C2\u05B5')
        line = line.replace('\u05B6\u05C2',u'\u05C2\u05B6')
        line = line.replace('\u05B7\u05C2',u'\u05C2\u05B7')
        line = line.replace('\u05B8\u05C2',u'\u05C2\u05B8')
        line = line.replace('\u05B9\u05C2',u'\u05C2\u05B9')
        line = line.replace('\u05BA\u05C2',u'\u05C2\u05BA')
        line = line.replace('\u05BB\u05C2',u'\u05C2\u05BB')
        # daghesh + sin/shin dot issues
        line = line.replace('\u05BC\u05C1',u'\u05C1\u05BC')
        line = line.replace('\u05BC\u05C2',u'\u05C2\u05BC')

        newFile.write(line)
