# twl_operations.py

import os
import sqlite3
import csv
import re

def parse_twl_file(file_path):
    book = os.path.splitext(os.path.basename(file_path))[0].split('_')[1]
    twl_data = []

    with open(file_path, 'r', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile, delimiter='\t')
        next(reader)  # Skip header row
        for row in reader:
            chapter, verse = map(int, row[0].split(':'))
            twl_data.append({
                'book': book,
                'chapter': chapter,
                'verse': verse,
                'twl_id': row[1],
                'tags': row[2],
                'OrigWords': row[3],
                'Occurrence': int(row[4]),
                'TWLink': row[5]
            })

    return twl_data

def insert_twl_data(db_path, twl_data):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    try:
        for entry in twl_data:
            # Insert into translation_words table
            cursor.execute('''
                INSERT INTO translation_words (book, chapter, verse, twl_id, tags, OrigWords, TWLink)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (entry['book'], entry['chapter'], entry['verse'], entry['twl_id'], entry['tags'], entry['OrigWords'], entry['TWLink']))
            
            translation_word_id = cursor.lastrowid

            # Split OrigWords into individual words
            orig_words = re.findall(r'\S+', re.sub(r'־', ' ', entry['OrigWords']))
            
            # Find matching sequence in Bible_Verse table
            placeholders = ', '.join(['?'] * len(orig_words))
            query = f'''
                SELECT id, Word
                FROM Bible_Verse
                WHERE Book = ? AND Chapter = ? AND Verse = ?
                  AND Word IN ({placeholders})
                ORDER BY id
            '''
            cursor.execute(query, (entry['book'], entry['chapter'], entry['verse']) + tuple(orig_words))
            
            matching_verses = cursor.fetchall()
            
            if len(matching_verses) >= len(orig_words):
                # Check if the sequence matches
                for i in range(len(matching_verses) - len(orig_words) + 1):
                    if [verse[1] for verse in matching_verses[i:i+len(orig_words)]] == orig_words:
                        # Found matching sequence, create links
                        for j, verse in enumerate(matching_verses[i:i+len(orig_words)]):
                            cursor.execute('''
                                INSERT INTO translation_word_links (translation_word_id, bible_verse_id, book, chapter, verse)
                                VALUES (?, ?, ?, ?, ?)
                            ''', (translation_word_id, verse[0], entry['book'], entry['chapter'], entry['verse']))
                        break
                else:
                    with open('error_log-b.txt', 'a', encoding='utf-8') as error_log:
                        error_log.write(f"No matching sequence found for {entry['book']} {entry['chapter']}:{entry['verse']}  {entry['twl_id']} - {entry['OrigWords']}\n")
            else:
                with open('error_log-b.txt', 'a', encoding='utf-8') as error_log:
                    error_log.write(f"Not enough matching words found for {entry['book']} {entry['chapter']}:{entry['verse']}  {entry['twl_id']} - {entry['OrigWords']}\n")

        conn.commit()
        print(f"Successfully inserted {len(twl_data)} TWL entries.")
    except Exception as e:
        conn.rollback()
        print(f"An error occurred: {str(e)}")
    finally:
        conn.close()

def process_twl_files(directory, db_path):
    for filename in os.listdir(directory):
        if filename.endswith('.tsv'):
            file_path = os.path.join(directory, filename)
            twl_data = parse_twl_file(file_path)
            insert_twl_data(db_path, twl_data)
            print(f"Processed {filename}")

                  
                   
                    # with open('error_log-b.txt', 'a', encoding='utf-8') as error_log:
                        # error_log.write(f"Nothing found in Bible_Verse found for {entry['book']} {entry['chapter']}:{entry['verse']} {entry['twl_id']}- {entry['OrigWords']} (occurrence {entry['Occurrence']})\n")



# Usage in main.py:
# from twl_operations import process_twl_files
# process_twl_files(config.TWL_DIRECTORY, db_path)