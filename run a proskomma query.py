
import subprocess, json, datetime, time
start_time = time.time()
pR = subprocess.run(['node','C:/Users/benja/Documents/GitHub/my_proskomma_tutorial/tutorial.js'], capture_output=True)
duration = time.time() - start_time
print(f"Proskomma took {duration} seconds")

start_time = time.time()
proskommaResults = pR.stdout.decode()
duration = time.time() - start_time
print(f"Decoding took {duration} seconds")

start_time = time.time()
with open("C:/Users/benja/Documents/GitHub/scriptoutput/prokomma.json", 'w', encoding='utf8') as f:
    f.write(proskommaResults)
duration = time.time() - start_time
print(f"Writing took {duration} seconds")

start_time = time.time()
resultDecoded = json.loads(proskommaResults)
duration = time.time() - start_time
print(f"Json loading took {duration} seconds")

# print(type(resultDecoded))

# This is a verse, it's a list, length equal to the number of verse: 
# ["data"]["documents"][0]["mainSequence"]["itemGroups"]
# 

start_time = time.time()

print(type(resultDecoded["data"]["documents"][0]["mainSequence"]["itemGroups"]))

verseItem = resultDecoded["data"]["documents"][0]["mainSequence"]["itemGroups"][0]

chapter = verseItem["chapter"][0].split('/')[1]
verse = verseItem["verse"][0].split('/')[1]
# print(f"{chapter}:{verse}")

alignedWords = resultDecoded["data"]["documents"][0]["mainSequence"]["itemGroups"][0]["tokens"]
# print(len(alignedWords))
# print(type(alignedWords))
original = alignedWords[0]["content"][0].rsplit('/', 1)[-1]
strongs = alignedWords[0]["strongs"][0].rsplit('/', 1)[-1]
alignedWord = alignedWords[0]["alignedWord"]

print(f"{original} with strongs {strongs} aligned to {alignedWord} in {chapter}:{verse}")

duration = time.time() - start_time
print(f"Python looking at the dictionary took {duration} seconds")
