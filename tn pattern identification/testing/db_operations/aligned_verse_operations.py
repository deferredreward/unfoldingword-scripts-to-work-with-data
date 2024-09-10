import sqlite3
import traceback

def insert_aligned_data(aligned_data, db_path, clear_table=False):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    try:
        if clear_table:
            cursor.execute('DELETE FROM Aligned_Verse')
            cursor.execute('DELETE FROM word_alignment')
            cursor.execute("DELETE FROM sqlite_sequence WHERE name='Aligned_Verse'")
            cursor.execute("DELETE FROM sqlite_sequence WHERE name='word_alignment'")
            print("Tables 'Aligned_Verse' and 'word_alignment' have been cleared and autoincrement counters reset.")

        seen_combinations = set()
        current_chapter = None
        inserted_count = 0
        current_book = None
        for book, chapter, verse, gl_word, gl_occurrence, gl_occurrences, x_content, h_occurrence, h_occurrences in aligned_data:
            if book != current_book:
                print(f"\nProcessing: {book} ", end="", flush=True) # Some user feedback
                current_book = book

            if chapter != current_chapter:
                seen_combinations = set()
                current_chapter = chapter
                print(f"{chapter}, ", end="", flush=True)

            unique_key = (book, chapter, verse, gl_word, gl_occurrence, gl_occurrences)

            # Check if this combination exists in Aligned_Verse
            cursor.execute('''
                SELECT id FROM Aligned_Verse
                WHERE Book = ? AND Chapter = ? AND Verse = ? AND Word = ? AND Occurrence = ? AND Occurrences = ?
            ''', (book, chapter, verse, gl_word, gl_occurrence, gl_occurrences))
            
            aligned_verse_result = cursor.fetchone()

            if aligned_verse_result:
                aligned_verse_id = aligned_verse_result[0]
            elif unique_key not in seen_combinations:
                seen_combinations.add(unique_key)
                cursor.execute('''
                    INSERT INTO Aligned_Verse (Book, Chapter, Verse, Word, Occurrence, Occurrences)
                    VALUES (?, ?, ?, ?, ?, ?)
                ''', (book, chapter, verse, gl_word, gl_occurrence, gl_occurrences))
                aligned_verse_id = cursor.lastrowid
            else:
                # Skip this entry if it's a duplicate within the chapter
                continue

            # Find corresponding Bible_Verse entry
            cursor.execute('''
                SELECT id, Word FROM Bible_Verse
                WHERE Book = ? AND Chapter = ? AND Verse = ? AND Word = ?
                ORDER BY id
                LIMIT ? OFFSET ?
            ''', (book, chapter, verse, x_content, 1, h_occurrence - 1))
           
            bible_verse_result = cursor.fetchone()
           
            if bible_verse_result:
                bible_verse_id, orig_word = bible_verse_result
                # Insert into word_alignment table
                cursor.execute('''
                    INSERT INTO word_alignment (bible_verse_id, aligned_verse_id, OrigL, GL)
                    VALUES (?, ?, ?, ?)
                ''', (bible_verse_id, aligned_verse_id, orig_word, gl_word))
                inserted_count += 1
            else:
                with open('error_log-b.txt', 'a', encoding='utf-8') as error_log:
                    error_log.write(f"No matching Bible_Verse found for {book} {chapter}:{verse} - {x_content} (occurrence {h_occurrence} of {h_occurrences})\n")

        conn.commit()
        print(f"Successfully inserted {inserted_count} entries into the word_alignment table.")
    except Exception as e:
        conn.rollback()
        print(f"An error occurred while inserting aligned data: {str(e)}")
        print("Exception details:")
        print(traceback.format_exc())
    finally:
        conn.close()