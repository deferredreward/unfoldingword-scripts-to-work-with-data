
import sqlite3
import traceback

def insert_word_alignments(alignments, db_path):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    try:
        cursor.executemany('''
            INSERT INTO word_alignment (bible_verse_id, aligned_verse_id)
            VALUES (?, ?)
        ''', alignments)

        conn.commit()
        print(f"Successfully inserted {len(alignments)} word alignments.")
    except Exception as e:
        conn.rollback()
        print(f"An error occurred while inserting word alignments: {str(e)}")
        print("Exception details:")
        print(traceback.format_exc())
    finally:
        conn.close()
        
def insert_bible_verses(words, db_path, clear_table=False):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    inserted_ids = []

    try:
        if clear_table:
            cursor.execute('DELETE FROM Bible_Verse')
            cursor.execute("DELETE FROM sqlite_sequence WHERE name='Bible_Verse'")
            print("Table 'Bible_Verse' has been cleared and autoincrement counter reset.")

        cursor.executemany('''
            INSERT INTO Bible_Verse (Book, Chapter, Verse, Word, Lemma, Strongs, Morphology)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', words)

        # Get the last inserted row id
        last_id = cursor.lastrowid
        # Calculate the ids of all inserted rows
        inserted_ids = list(range(last_id - len(words) + 1, last_id + 1))

        conn.commit()
        print(f"Successfully inserted {len(words)} words into the Bible_Verse table.")
    except Exception as e:
        conn.rollback()
        print(f"An error occurred: {str(e)}")
        print("Exception details:")
        print(traceback.format_exc())
    finally:
        conn.close()

    return inserted_ids
