import os
import sqlite3

def create_tables(cursor):
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Bible_Verse (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        Book TEXT,
        Chapter INTEGER,
        Verse INTEGER,
        Word TEXT,
        Lemma TEXT,
        Strongs TEXT,
        Morphology TEXT
    )
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Aligned_Verse (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        Book TEXT,
        Chapter INTEGER,
        Verse INTEGER,
        Word TEXT,
        Occurrence INTEGER,
        Occurrences INTEGER
    )
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS word_alignment (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        bible_verse_id INTEGER,
        aligned_verse_id INTEGER,
        OrigL TEXT,
        GL TEXT,
        FOREIGN KEY (bible_verse_id) REFERENCES Bible_Verse(id),
        FOREIGN KEY (aligned_verse_id) REFERENCES Aligned_Verse(id)
    )
    ''')
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS translation_words (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        book TEXT,
        chapter INTEGER,
        verse INTEGER,
        twl_id TEXT,
        tags TEXT,
        OrigWords TEXT,
        TWLink TEXT
    )
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS translation_word_links (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        book TEXT,
        chapter INTEGER,
        verse INTEGER,
        translation_word_id INTEGER,
        bible_verse_id INTEGER,
        FOREIGN KEY (translation_word_id) REFERENCES translation_words(id),
        FOREIGN KEY (bible_verse_id) REFERENCES Bible_Verse(id)
    )
    ''')
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS translation_notes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        book TEXT,
        chapter INTEGER,
        verse INTEGER,
        tn_id TEXT,
        support_reference TEXT,
        quote TEXT,
        occurrence INTEGER,
        note TEXT
    )
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS translation_note_links (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        book TEXT,
        chapter INTEGER,
        verse INTEGER,
        translation_note_id INTEGER,
        bible_verse_id INTEGER,
        FOREIGN KEY (translation_note_id) REFERENCES translation_notes(id),
        FOREIGN KEY (bible_verse_id) REFERENCES Bible_Verse(id)
    )
    ''')

def get_next_db_name(base_name="BookPackage"):
    i = 1
    while True:
        db_name = f"{base_name}{i}.db"
        if not os.path.exists(db_name):
            return db_name
        i += 1

def prepare_db(db_name=None):
    if not db_name:
        db_name = get_next_db_name()    
        print(f"Creating database: {db_name}")
    else: print(f"Using database: {db_name}")
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    create_tables(cursor)
    conn.commit()
    conn.close()    
    return db_name