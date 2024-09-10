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

def get_next_db_name(base_name="BookPackage"):
    i = 1
    while True:
        db_name = f"{base_name}{i}.db"
        if not os.path.exists(db_name):
            return db_name
        i += 1

def create_new_db():
    db_name = get_next_db_name()
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    create_tables(cursor)
    conn.commit()
    conn.close()
    print(f"Created new database: {db_name}")
    return db_name