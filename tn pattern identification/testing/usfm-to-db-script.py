import os
import re
import sqlite3
import traceback

# def insert_into_db(words, db_path, clear_table=False):
#     conn = sqlite3.connect(db_path)
#     cursor = conn.cursor()

#     try:
#         if clear_table:
#             cursor.execute('DELETE FROM Bible_Verse')
#             cursor.execute("DELETE FROM sqlite_sequence WHERE name='Bible_Verse'")
#             print("Table 'Bible_Verse' has been cleared and autoincrement counter reset.")

#         cursor.executemany('''
#             INSERT INTO Bible_Verse (Book, Chapter, Verse, Word, Lemma, Strongs, Morphology)
#             VALUES (?, ?, ?, ?, ?, ?, ?)
#         ''', words)

#         conn.commit()
#         print(f"Successfully inserted {len(words)} words into the Bible_Verse table.")
#     except Exception as e:
#         conn.rollback()
#         print(f"An error occurred: {str(e)}")
#         print("Exception details:")
#         print(traceback.format_exc())
#     finally:
#         conn.close()

# def parse_usfm_file(file_path):
#     with open(file_path, 'r', encoding='utf-8') as file:
#         content = file.read()

#     book = re.search(r'\\id\s+([A-Z]{3})', content)
#     book = book.group(1) if book else "Unknown"
#     verses = []
#     current_chapter = 1
#     current_verse = 1

#     for line in content.split('\n'):
#         if line.startswith('\\c '):
#             current_chapter = int(line.split()[1])
#         elif line.startswith('\\v '):
#             current_verse = int(line.split()[1])
#         words = re.findall(r'\\w (.*?)\|lemma="(.*?)" strong="(.*?)" x-morph="He,(.*?)"\\w\*', line)
#         for word, lemma, strong, morph in words:
#             verses.append((book, current_chapter, current_verse, word, lemma, strong, morph))
#     return verses

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

# def parse_aligned_usfm(file_path):
#     try:
#         with open(file_path, 'r', encoding='utf-8') as file:
#             content = file.read()

#         book = re.search(r'\\id\s+([A-Z]{3})', content)
#         book = book.group(1) if book else "Unknown"
#         aligned_words = []
#         current_chapter = 1
#         current_verse = 1

#         # Split content into verses
#         verses = re.split(r'\\v\s+(\d+)\s*', content)[1:]  # This will give us pairs of (verse number, verse content)

#         for i in range(0, len(verses), 2):
#             current_verse = int(verses[i])
#             verse_content = verses[i+1]
            
#             # Extract all zaln-s blocks
#             zaln_starts = list(re.finditer(r'\\zaln-s\s+\|([^\\]*)', verse_content))
            
#             for j, start_match in enumerate(zaln_starts):
#                 try:
#                     # Find the corresponding zaln-e
#                     end_index = verse_content.find('\\zaln-e', start_match.end())
#                     if end_index == -1:
#                         print(f"Warning: No closing zaln-e found for zaln-s in {book} {current_chapter}:{current_verse}")
#                         continue
                    
#                     zaln_block = verse_content[start_match.start():end_index + 8]  # +8 to include '\\zaln-e'
                    
#                     # Extract Hebrew word info (x-content only)
#                     hebrew_attrs = start_match.group(1)
#                     x_content = re.search(r'x-content="([^"]*)"', hebrew_attrs)
#                     x_content = x_content.group(1) if x_content else ""

#                     # Extract English words with their occurrence info
#                     gl_words = re.finditer(r'\\w\s+([^|\\]*?)\|([^\\]*?)\\w\*', zaln_block)
                    
#                     for gl_word_match in gl_words:
#                         gl_word = gl_word_match.group(1).strip()
#                         gl_attrs = gl_word_match.group(2)
                        
#                         occurrence = re.search(r'x-occurrence="(\d+)"', gl_attrs)
#                         occurrence = int(occurrence.group(1)) if occurrence else 1
                        
#                         occurrences = re.search(r'x-occurrences="(\d+)"', gl_attrs)
#                         occurrences = int(occurrences.group(1)) if occurrences else 1

#                         aligned_words.append((book, current_chapter, current_verse, x_content, gl_word, occurrence, occurrences))
                
#                 except Exception as e:
#                     print(f"Error processing zaln block in {book} {current_chapter}:{current_verse}")
#                     print(f"zaln block content: {zaln_block}")
#                     print(f"Error: {str(e)}")

#             # Check for chapter changes
#             chapter_match = re.search(r'\\c\s+(\d+)', verse_content)
#             if chapter_match:
#                 current_chapter = int(chapter_match.group(1))

#         if not aligned_words:
#             print(f"No aligned verses found in file: {file_path}")
#         else:
#             print(f"Found {len(aligned_words)} aligned words in file: {file_path}")
            
#         # Print some sample data for verification
#         # print("Sample aligned data (first 10 entries):")
#         # for entry in aligned_verses[:10]:
#         #     print(entry)

#         return aligned_words

#     except Exception as e:
#         print(f"Error processing file {file_path}: {str(e)}")
#         print("Exception details:")
#         print(traceback.format_exc())
#         return []

def process_aligned_usfm_files(directory, db_path):
    all_aligned_verses = []
    for filename in os.listdir(directory):
        if filename.endswith('.usfm'):
            file_path = os.path.join(directory, filename)
            try:
                aligned_verses = parse_aligned_usfm(file_path)
                all_aligned_verses.extend(aligned_verses)
                print(f"Processed {filename}: Found {len(aligned_verses)} aligned words")
            except Exception as e:
                print(f"Error processing aligned file {filename}: {str(e)}")
                print("Exception details:")
                print(traceback.format_exc())

    if all_aligned_verses:
        clear_table = input("Do you want to clear the Aligned_Verse table before inserting new data? (y/n): ").lower() == 'y'
        insert_aligned_data(all_aligned_verses, db_path, clear_table)
    else:
        print("No aligned verses were parsed. Check the USFM files and error messages.")

def insert_aligned_data(aligned_data, db_path, clear_table=False):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    try:
        if clear_table:
            cursor.execute('DELETE FROM Aligned_Verse')
            cursor.execute("DELETE FROM sqlite_sequence WHERE name='Aligned_Verse'")
            print("Table 'Aligned_Verse' has been cleared and autoincrement counter reset.")

        for book, chapter, verse, x_content, gl_word, occurrence, occurrences in aligned_data:
            cursor.execute('''
                SELECT id FROM Bible_Verse
                WHERE Book = ? AND Chapter = ? AND Verse = ? AND Word = ?
            ''', (book, chapter, verse, x_content))
            
            bible_verse_id = cursor.fetchone()
            
            if bible_verse_id:
                cursor.execute('''
                    INSERT INTO Aligned_Verse (bible_verse_id, GLword, occurrence, occurrences)
                    VALUES (?, ?, ?, ?)
                ''', (bible_verse_id[0], gl_word, occurrence, occurrences))
            else:
                print(f"No matching Bible_Verse found for {book} {chapter}:{verse} - {x_content}")

        conn.commit()
        print(f"Successfully inserted {len(aligned_data)} aligned words into the Aligned_Verse table.")
    except Exception as e:
        conn.rollback()
        print(f"An error occurred while inserting aligned data: {str(e)}")
        print("Exception details:")
        print(traceback.format_exc())
    finally:
        conn.close()

if __name__ == "__main__":
    origL_usfm_directory = "C:/Users/benja/Documents/GitHub/unfoldingword-scripts-to-work-with-data/tn pattern identification/testing/data/origL"
    aligned_usfm_directory = "C:/Users/benja/Documents/GitHub/unfoldingword-scripts-to-work-with-data/tn pattern identification/testing/data/ult"
    db_path = "C:/Users/benja/Documents/GitHub/unfoldingword-scripts-to-work-with-data/tn pattern identification/testing/data/aligned-bible-with-tns-twls.db"
    
    process_origL_usfm_files(origL_usfm_directory, db_path)
    process_aligned_usfm_files(aligned_usfm_directory, db_path)
