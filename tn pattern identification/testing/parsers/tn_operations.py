# tn_operations.py

import os
import sqlite3
import csv
import re
import logging

logging.basicConfig(filename='tn_parsing.log', level=logging.INFO)

def parse_tn_file(file_path):
    book = os.path.splitext(os.path.basename(file_path))[0].split('_')[1]
    tn_data = []

    with open(file_path, 'r', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile, delimiter='\t')
        next(reader)  # Skip header row
        for row in reader:
            # Skip intro rows and rows with occurrence 0
            if row[0].startswith('front:') or ':intro' in row[0]:
                continue

            # Handle empty or non-digit occurrence
            occurrence = int(row[5]) if row[5].isdigit() else 1

            # Skip rows with occurrence 0
            if occurrence == 0:
                continue
            # Check for well-formed chapter and verse
            try:
                chapter, verse = map(int, row[0].split(':'))
            except ValueError:
                # Skip rows with complex verse ranges or malformed chapter:verse
                logging.info(f"Skipped row with complex verse range: {book} {row}")
                continue

            support_reference = row[3].split('/')[-1] if row[3] else ''
            
            tn_data.append({
                'book': book,
                'chapter': chapter,
                'verse': verse,
                'tn_id': row[1],
                'support_reference': support_reference,
                'quote': row[4],
                'occurrence': occurrence,
                'note': row[6]
            })

    return tn_data

def insert_tn_data(db_path, tn_data):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    inserted_count = 0
    skipped_count = 0

    try:
        for entry in tn_data:
            # Check if this tn_id already exists for this book
            cursor.execute('''
                SELECT COUNT(*) FROM translation_notes
                WHERE book = ? AND tn_id = ?
            ''', (entry['book'], entry['tn_id']))
            
            if cursor.fetchone()[0] > 0:
                # Duplicate found, log it and skip
                with open('error_log-tn.txt', 'a', encoding='utf-8') as error_log:
                    error_log.write(f"Duplicate entry skipped: Book {entry['book']}, Chapter {entry['chapter']}, Verse {entry['verse']}, tn_id {entry['tn_id']}\n")
                skipped_count += 1
                continue

            # Insert into translation_notes table
            cursor.execute('''
                INSERT INTO translation_notes (book, chapter, verse, tn_id, support_reference, quote, occurrence, note)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ''', (entry['book'], entry['chapter'], entry['verse'], entry['tn_id'], entry['support_reference'], 
                  entry['quote'], entry['occurrence'], entry['note']))
            
            translation_note_id = cursor.lastrowid

            # Handle quotes
            quote_parts = [part.strip() for part in entry['quote'].split('&')]
            
            for part in quote_parts:
                orig_words = re.findall(r'\S+', re.sub(r'[־׃׀,.?;!()—:]', ' ', part))
                
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
                
                if matching_verses:
                    # Check if the sequence matches, allowing for partial matches and skipping punctuation
                    i = 0
                    j = 0
                    while i < len(matching_verses) and j < len(orig_words):
                        bible_word = re.sub(r'[־׃׀]', '', matching_verses[i][1])
                        orig_word = re.sub(r'[־׃׀]', '', orig_words[j])
                        
                        if bible_word == orig_word or bible_word.startswith(orig_word) or orig_word.startswith(bible_word):
                            cursor.execute('''
                                INSERT INTO translation_note_links (translation_note_id, bible_verse_id, book, chapter, verse)
                                VALUES (?, ?, ?, ?, ?)
                            ''', (translation_note_id, matching_verses[i][0], entry['book'], entry['chapter'], entry['verse']))
                            i += 1
                            j += 1
                        else:
                            i += 1
                    
                    if j < len(orig_words):
                        with open('error_log-tn.txt', 'a', encoding='utf-8') as error_log:
                            error_log.write(f"Partial match found for {entry['book']} {entry['chapter']}:{entry['verse']} {entry['tn_id']} - {part}\n")
                else:
                    with open('error_log-tn.txt', 'a', encoding='utf-8') as error_log:
                        error_log.write(f"No matching words found for {entry['book']} {entry['chapter']}:{entry['verse']} {entry['tn_id']} - {part}\n")

        conn.commit()
        print(f"Successfully inserted {inserted_count} TN entries. Skipped {skipped_count} duplicate entries.")
    except Exception as e:
        conn.rollback()
        print(f"An error occurred: {str(e)}")
    finally:
        conn.close()

def process_tn_files(directory, db_path, clear_table=False):
    if clear_table:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute('DELETE FROM translation_notes')
        cursor.execute('DELETE FROM translation_note_links')
        cursor.execute("DELETE FROM sqlite_sequence WHERE name='translation_notes'")
        cursor.execute("DELETE FROM sqlite_sequence WHERE name='translation_note_links'")
        print("Tables 'translation_note' and 'translation_note_links' have been cleared and autoincrement counters reset.")
        conn.close()

    for filename in os.listdir(directory):
        if filename.endswith('.tsv'):
            file_path = os.path.join(directory, filename)
            tn_data = parse_tn_file(file_path)
            insert_tn_data(db_path, tn_data)
            print(f"Processed {filename}")