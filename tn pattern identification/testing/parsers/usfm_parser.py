import re


def parse_usfm_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()

    book = re.search(r'\\id\s+([1-3]?[A-Z]{2,3})', content)
    book = book.group(1) if book else "Unknown"
    verses = []
    current_chapter = 1
    current_verse = 1

    for line in content.split('\n'):
        if line.startswith('\\c '):
            current_chapter = int(line.split()[1])
        elif line.startswith('\\v '):
            current_verse = int(line.split()[1])
        words = re.findall(r'\\w (.*?)\|lemma="(.*?)" strong="(.*?)" x-morph="[AHGer]{2},(.*?)" ?\\w\*', line)
        for word, lemma, strong, morph in words:
            verses.append((book, current_chapter, current_verse, word, lemma, strong, morph))
    return verses
