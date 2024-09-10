import os
import re
import sqlite3
from collections import defaultdict
import traceback

def parse_usfm_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()

    book = re.search(r'\\id\s+([A-Z]{3})', content)
    book = book.group(1) if book else "Unknown"
    verses = []
    current_chapter = 1
    current_verse = 1

    for line in content.split('\n'):
        if line.startswith('\\c '):
            current_chapter = int(line.split()[1])
        elif line.startswith('\\v '):
            current_verse = int(line.split()[1])
        words = re.findall(r'\\w (.*?)\|lemma="(.*?)" strong="(.*?)" x-morph="He,(.*?)"\\w\*', line)
        for word, lemma, strong, morph in words:
            verses.append((book, current_chapter, current_verse, word, lemma, strong, morph))
    return verses

def insert_into_db(words, db_path, clear_table=False):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    if clear_table:
        cursor.execute('DELETE FROM Bible_Verse')
        # Reset the autoincrement counter for Bible_Verse table
        cursor.execute("DELETE FROM sqlite_sequence WHERE name='Bible_Verse'")
        print("Table 'Bible_Verse' has been cleared and autoincrement counter reset.")

    cursor.executemany('''
        INSERT INTO Bible_Verse (Book, Chapter, Verse, Word, Lemma, Strongs, Morphology)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', words)

    conn.commit()
    print(f"Successfully inserted {len(words)} words into the database.")
    conn.close()

def process_origL_usfm_files(directory, db_path):
    all_verses = []
    for filename in os.listdir(directory):
        if filename.endswith('.usfm'):
            file_path = os.path.join(directory, filename)
            try:
                verses = parse_usfm_file(file_path)
                all_verses.extend(verses)
            except Exception as e:
                print(f"Error processing file {filename}: {str(e)}")
                print("Exception details:")
                print(traceback.format_exc())

    if all_verses:
        clear_table = input("Do you want to clear the Bible_Verse table before inserting new data? (y/n): ").lower() == 'y'
        insert_into_db(all_verses, db_path, clear_table)
    else:
        print("No verses were parsed. Check the USFM files and error messages.")

if __name__ == "__main__":
    origL_usfm_directory = "C:/Users/benja/Documents/GitHub/unfoldingword-scripts-to-work-with-data/tn pattern identification/testing/origL"
    db_path = "C:/Users/benja/Documents/GitHub/unfoldingword-scripts-to-work-with-data/tn pattern identification/testing/aligned-bible-with-tns-twls.db"
    process_origL_usfm_files(origL_usfm_directory, db_path)


