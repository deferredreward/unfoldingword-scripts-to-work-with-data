import re
import sqlite3
import os

def create_tables(conn):
    c = conn.cursor()
    
    c.execute('''CREATE TABLE IF NOT EXISTS Document
                 (id INTEGER PRIMARY KEY, book_code TEXT, book_name TEXT)''')
    
    c.execute('''CREATE TABLE IF NOT EXISTS Verse
                 (id INTEGER PRIMARY KEY, document_id INTEGER, chapter INTEGER, verse INTEGER, 
                  content TEXT, FOREIGN KEY(document_id) REFERENCES Document(id))''')
    
    c.execute('''CREATE TABLE IF NOT EXISTS Word
                 (id INTEGER PRIMARY KEY, verse_id INTEGER, position INTEGER, 
                  text TEXT, occurrence INTEGER, occurrences INTEGER, 
                  FOREIGN KEY(verse_id) REFERENCES Verse(id))''')
    
    c.execute('''CREATE TABLE IF NOT EXISTS Alignment
                 (id INTEGER PRIMARY KEY, verse_id INTEGER, start_word_position INTEGER, 
                  end_word_position INTEGER, strong_number TEXT, lemma TEXT, morph TEXT, 
                  occurrence INTEGER, occurrences INTEGER, content TEXT, 
                  FOREIGN KEY(verse_id) REFERENCES Verse(id))''')
    
    c.execute('''CREATE TABLE IF NOT EXISTS Tag
                 (id INTEGER PRIMARY KEY, verse_id INTEGER, tag_name TEXT, position INTEGER, 
                  FOREIGN KEY(verse_id) REFERENCES Verse(id))''')
    
    conn.commit()

def insert_document(conn, book_code, book_name):
    c = conn.cursor()
    c.execute("INSERT INTO Document (book_code, book_name) VALUES (?, ?)", (book_code, book_name))
    return c.lastrowid

def insert_verse(conn, document_id, chapter, verse, content):
    c = conn.cursor()
    c.execute("INSERT INTO Verse (document_id, chapter, verse, content) VALUES (?, ?, ?, ?)",
              (document_id, chapter, verse, content))
    return c.lastrowid

def insert_word(conn, verse_id, position, text, occurrence, occurrences):
    c = conn.cursor()
    c.execute("INSERT INTO Word (verse_id, position, text, occurrence, occurrences) VALUES (?, ?, ?, ?, ?)",
              (verse_id, position, text, occurrence, occurrences))

def insert_alignment(conn, verse_id, start_pos, end_pos, strong, lemma, morph, occurrence, occurrences, content):
    c = conn.cursor()
    c.execute('''INSERT INTO Alignment 
                 (verse_id, start_word_position, end_word_position, strong_number, lemma, morph, occurrence, occurrences, content) 
                 VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)''',
              (verse_id, start_pos, end_pos, strong, lemma, morph, occurrence, occurrences, content))

def insert_tag(conn, verse_id, tag_name, position):
    c = conn.cursor()
    c.execute("INSERT INTO Tag (verse_id, tag_name, position) VALUES (?, ?, ?)",
              (verse_id, tag_name, position))

def parse_usfm(usfm_content):
    lines = usfm_content.split('\n')
    book_code = ''
    book_name = ''
    current_chapter = 0
    current_verse = 0
    
    verses = []
    current_verse_content = ''

    for line in lines:
        if line.startswith('\\id '):
            book_code = line.split()[1]
        elif line.startswith('\\h '):
            book_name = line[3:].strip()
        elif line.startswith('\\c '):
            current_chapter = int(line.split()[1])
        elif line.startswith('\\v '):
            if current_verse_content:
                verses.append((current_chapter, current_verse, current_verse_content.strip()))
            current_verse = int(line.split()[1])
            current_verse_content = line[line.index(' ', 3)+1:]
        else:
            current_verse_content += ' ' + line.strip()

    if current_verse_content:
        verses.append((current_chapter, current_verse, current_verse_content.strip()))

    return book_code, book_name, verses

def safe_int(value):
    try:
        return int(value.strip('"'))
    except ValueError:
        return 1  # Default value if conversion fails

def process_usfm(usfm_file, db_file):
    with open(usfm_file, 'r', encoding='utf-8') as file:
        usfm_content = file.read()
    
    book_code, book_name, verses = parse_usfm(usfm_content)
    
    conn = sqlite3.connect(db_file)
    create_tables(conn)
    
    doc_id = insert_document(conn, book_code, book_name)
    
    for chapter, verse_num, content in verses:
        verse_id = insert_verse(conn, doc_id, chapter, verse_num, content)
        
        word_position = 0
        tag_position = 0
        
        words = re.findall(r'\\w ([^|]+)\|([^\\]+)\\w\*', content)
        for word, attributes in words:
            word_position += 1
            attr_dict = dict(item.split('=') for item in attributes.split() if '=' in item)
            insert_word(conn, verse_id, word_position, word,
                        safe_int(attr_dict.get('x-occurrence', '1')),
                        safe_int(attr_dict.get('x-occurrences', '1')))

        alignments = re.findall(r'\\zaln-s ([^\\]+)\\*', content)
        for alignment in alignments:
            attr_dict = dict(item.split('=') for item in alignment.split() if '=' in item)
            insert_alignment(conn, verse_id, word_position, word_position,
                             attr_dict.get('x-strong'), attr_dict.get('x-lemma'),
                             attr_dict.get('x-morph'),
                             safe_int(attr_dict.get('x-occurrence', '1')),
                             safe_int(attr_dict.get('x-occurrences', '1')),
                             attr_dict.get('x-content'))

        tags = re.findall(r'\\(q1|q2|ts)', content)
        for tag in tags:
            tag_position += 1
            insert_tag(conn, verse_id, tag, tag_position)
    
    conn.commit()
    conn.close()

# Usage
usfm_file = '31-OBA.usfm'
db_file = 'output_database.sqlite'

# Check if the database file already exists
if os.path.exists(db_file):
    user_input = input(f"The file {db_file} already exists. Do you want to overwrite it? (y/n): ")
    if user_input.lower() != 'y':
        print("Operation cancelled.")
        exit()
    else:
        os.remove(db_file)
        print(f"Existing {db_file} has been removed. Creating a new database.")

process_usfm(usfm_file, db_file)
print(f"Database has been created/updated at {db_file}")