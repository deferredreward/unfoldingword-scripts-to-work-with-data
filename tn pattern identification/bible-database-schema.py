# -- Database Schema

# -- Table for storing the basic text structure
# CREATE TABLE verses (
#     id INTEGER PRIMARY KEY,
#     book TEXT,
#     chapter INTEGER,
#     verse INTEGER,
#     text TEXT
# );

# -- Table for storing individual words/phrases
# CREATE TABLE words (
#     id INTEGER PRIMARY KEY,
#     verse_id INTEGER,
#     word_number INTEGER,
#     content TEXT,
#     lemma TEXT,
#     strong TEXT,
#     morph TEXT,
#     FOREIGN KEY (verse_id) REFERENCES verses(id)
# );

# -- Table for storing translation notes
# CREATE TABLE translation_notes (
#     id INTEGER PRIMARY KEY,
#     verse_id INTEGER,
#     note_id TEXT,
#     category TEXT,
#     rc_link TEXT,
#     aligned_content TEXT,
#     occurrence INTEGER,
#     note_text TEXT,
#     FOREIGN KEY (verse_id) REFERENCES verses(id)
# );

# -- Table for storing keyword/name data
# CREATE TABLE keywords (
#     id INTEGER PRIMARY KEY,
#     verse_id INTEGER,
#     note_id TEXT,
#     category TEXT,
#     aligned_content TEXT,
#     occurrence INTEGER,
#     rc_link TEXT,
#     FOREIGN KEY (verse_id) REFERENCES verses(id)
# );

# -- Python code for parsing and inserting data

import re
import sqlite3

def parse_usfm(usfm_text):
    # This is a simplified parser and would need to be more robust for production use
    verse_pattern = r'\\v\s+(\d+)\s+(.*?)(?=\\v|\Z)'
    word_pattern = r'\\zaln-s\s+\|x-strong="([^"]+)"\s+x-lemma="([^"]+)"\s+x-morph="([^"]+)"[^>]*>(.*?)\\zaln-e\*'
    
    verses = re.findall(verse_pattern, usfm_text, re.DOTALL)
    print(str(verses))
    conn = sqlite3.connect('bible_database.db')
    cursor = conn.cursor()
    
    for verse_num, verse_content in verses:
        cursor.execute('INSERT INTO verses (book, chapter, verse, text) VALUES (?, ?, ?, ?)',
                       ('Obadiah', 1, int(verse_num), verse_content))
        verse_id = cursor.lastrowid
        
        words = re.findall(word_pattern, verse_content)
        for word_num, (strong, lemma, morph, content) in enumerate(words, 1):
            cursor.execute('INSERT INTO words (verse_id, word_number, content, lemma, strong, morph) VALUES (?, ?, ?, ?, ?, ?)',
                           (verse_id, word_num, content, lemma, strong, morph))
    
    conn.commit()
    conn.close()

def parse_translation_notes(notes_text):
    note_pattern = r'(\d+:\d+)\s+(\w+)\s+(rc://[^\s]+)\s+(.*?)\s+(\d+)\s+(.*)'
    
    conn = sqlite3.connect('bible_database.db')
    cursor = conn.cursor()
    
    for line in notes_text.split('\n'):
        match = re.match(note_pattern, line)
        if match:
            verse_ref, note_id, rc_link, aligned_content, occurrence, note_text = match.groups()
            chapter, verse = map(int, verse_ref.split(':'))
            
            cursor.execute('SELECT id FROM verses WHERE book = ? AND chapter = ? AND verse = ?',
                           ('Obadiah', chapter, verse))
            verse_id = cursor.fetchone()[0]
            
            cursor.execute('INSERT INTO translation_notes (verse_id, note_id, category, rc_link, aligned_content, occurrence, note_text) VALUES (?, ?, ?, ?, ?, ?, ?)',
                           (verse_id, note_id, 'translation_note', rc_link, aligned_content, int(occurrence), note_text))
    
    conn.commit()
    conn.close()

def parse_keywords(keywords_text):
    keyword_pattern = r'(\d+:\d+)\s+(\w+)\s+(\w+)\s+(.*?)\s+(\d+)\s+(rc://.*)'
    
    conn = sqlite3.connect('bible_database.db')
    cursor = conn.cursor()
    
    for line in keywords_text.split('\n'):
        match = re.match(keyword_pattern, line)
        if match:
            verse_ref, note_id, category, aligned_content, occurrence, rc_link = match.groups()
            chapter, verse = map(int, verse_ref.split(':'))
            
            cursor.execute('SELECT id FROM verses WHERE book = ? AND chapter = ? AND verse = ?',
                           ('Obadiah', chapter, verse))
            verse_id = cursor.fetchone()[0]
            
            cursor.execute('INSERT INTO keywords (verse_id, note_id, category, aligned_content, occurrence, rc_link) VALUES (?, ?, ?, ?, ?, ?)',
                           (verse_id, note_id, category, aligned_content, int(occurrence), rc_link))
    
    conn.commit()
    conn.close()

# Usage example:
usfm_text = """
\v 1 \zaln-s |x-strong="H2377" x-lemma="חָזוֹן" x-morph="He,Ncmsc" x-occurrence="1" x-occurrences="1" x-content="חֲז֖וֹן"\*\w The|x-occurrence="1" x-occurrences="1"\w*
\w vision|x-occurrence="1" x-occurrences="1"\w*
\w of|x-occurrence="1" x-occurrences="1"\w*\zaln-e\*
\zaln-s |x-strong="H5662" x-lemma="עֹבַדְיָה" x-morph="He,Np" x-occurrence="1" x-occurrences="1" x-content="עֹֽבַדְיָ֑ה"\*\w Obadiah|x-occurrence="1" x-occurrences="1"\w*\zaln-e\*:
\zaln-s |x-strong="H3541" x-lemma="כֹּה" x-morph="He,D" x-occurrence="1" x-occurrences="1" x-content="כֹּֽה"\*\w thus|x-occurrence="1" x-occurrences="1"\w*\zaln-e\*
\zaln-s |x-strong="H0559" x-lemma="אָמַר" x-morph="He,Vqp3ms" x-occurrence="1" x-occurrences="1" x-content="אָמַר֩"\*\w says|x-occurrence="1" x-occurrences="1"\w*\zaln-e\*
\zaln-s |x-strong="H0136" x-lemma="אֲדֹנָי" x-morph="He,Ncmpc:Sp1cs" x-occurrence="1" x-occurrences="1" x-content="אֲדֹנָ֨⁠י"\*\w my|x-occurrence="1" x-occurrences="1"\w*
\w Lord|x-occurrence="1" x-occurrences="1"\w*\zaln-e\*
\zaln-s |x-strong="H3069" x-lemma="יְהֹוִה" x-morph="He,Np" x-occurrence="1" x-occurrences="1" x-content="יְהוִ֜ה"\*\w Yahweh|x-occurrence="1" x-occurrences="2"\w*\zaln-e\*
\zaln-s |x-strong="l:H0123" x-lemma="אֱדֹם" x-morph="He,R:Np" x-occurrence="1" x-occurrences="1" x-content="לֶ⁠אֱד֗וֹם"\*\w concerning|x-occurrence="1" x-occurrences="1"\w*
\w Edom|x-occurrence="1" x-occurrences="1"\w*\zaln-e\*.
\q1 \zaln-s |x-strong="H8085" x-lemma="שָׁמַע" x-morph="He,Vqp1cp" x-occurrence="1" x-occurrences="1" x-content="שָׁמַ֜עְנוּ"\*\w We|x-occurrence="1" x-occurrences="1"\w*
\w have|x-occurrence="1" x-occurrences="1"\w*
\w heard|x-occurrence="1" x-occurrences="1"\w*\zaln-e\*
\zaln-s |x-strong="H8052" x-lemma="שְׁמוּעָה" x-morph="He,Ncfsa" x-occurrence="1" x-occurrences="1" x-content="שְׁמוּעָ֨ה"\*\w a|x-occurrence="1" x-occurrences="2"\w*
\w message|x-occurrence="1" x-occurrences="1"\w*\zaln-e\*
\zaln-s |x-strong="m:H0854" x-lemma="אֵת" x-morph="He,R:R" x-occurrence="1" x-occurrences="1" x-content="מֵ⁠אֵ֤ת"\*\w from|x-occurrence="1" x-occurrences="1"\w*\zaln-e\*
\zaln-s |x-strong="H3068" x-lemma="יְהֹוָה" x-morph="He,Np" x-occurrence="1" x-occurrences="1" x-content="יְהוָה֙"\*\w Yahweh|x-occurrence="2" x-occurrences="2"\w*\zaln-e\*,
\zaln-s |x-strong="c:H6735a" x-lemma="צִיר" x-morph="He,C:Ncmsa" x-occurrence="1" x-occurrences="1" x-content="וְ⁠צִיר֙"\*\w and|x-occurrence="1" x-occurrences="1"\w*
\w a|x-occurrence="2" x-occurrences="2"\w*
\w messenger|x-occurrence="1" x-occurrences="1"\w*\zaln-e\*
\zaln-s |x-strong="H7971" x-lemma="שָׁלַח" x-morph="He,VPp3ms" x-occurrence="1" x-occurrences="1" x-content="שֻׁלָּ֔ח"\*\w has|x-occurrence="1" x-occurrences="1"\w*
\w been|x-occurrence="1" x-occurrences="1"\w*
\w sent|x-occurrence="1" x-occurrences="1"\w*
\w off|x-occurrence="1" x-occurrences="1"\w*\zaln-e\*
\zaln-s |x-strong="b:H1471a" x-lemma="גּוֹי" x-morph="He,Rd:Ncmpa" x-occurrence="1" x-occurrences="1" x-content="בַּ⁠גּוֹיִ֣ם"\*\w among|x-occurrence="1" x-occurrences="1"\w*
\w the|x-occurrence="1" x-occurrences="1"\w*
\w nations|x-occurrence="1" x-occurrences="1"\w*\zaln-e\*:
\q2 \zaln-s |x-strong="H6965b" x-lemma="קוּם" x-morph="He,Vqv2mp" x-occurrence="1" x-occurrences="1" x-content="ק֛וּמוּ"\*\w Get|x-occurrence="1" x-occurrences="1"\w*
\w up|x-occurrence="1" x-occurrences="2"\w*\zaln-e\*!
\zaln-s |x-strong="c:H6965b" x-lemma="קוּם" x-morph="He,C:Vqh1cp" x-occurrence="1" x-occurrences="1" x-content="וְ⁠נָק֥וּמָה"\*\w And|x-occurrence="1" x-occurrences="1"\w*
\w let|x-occurrence="1" x-occurrences="1"\w*
\w us|x-occurrence="1" x-occurrences="1"\w*
\w rise|x-occurrence="1" x-occurrences="1"\w*
\w up|x-occurrence="2" x-occurrences="2"\w*\zaln-e\*
\zaln-s |x-strong="H5921a" x-lemma="עַל" x-morph="He,R:Sp3fs" x-occurrence="1" x-occurrences="1" x-content="עָלֶי⁠הָ"\*\w against|x-occurrence="1" x-occurrences="1"\w*
\w her|x-occurrence="1" x-occurrences="1"\w*\zaln-e\*
\zaln-s |x-strong="l:H4421" x-lemma="מִלְחָמָה" x-morph="He,Rd:Ncfsa" x-occurrence="1" x-occurrences="1" x-content="לַ⁠מִּלְחָמָֽה"\*\w for|x-occurrence="1" x-occurrences="1"\w*
\w battle|x-occurrence="1" x-occurrences="1"\w*\zaln-e\*!
"""
parse_usfm(usfm_text)

translation_notes = """
1:1 xm1w        rc://*/ta/man/translate/figs-metaphor   חֲז֖וֹן עֹֽבַדְיָ֑ה 1   This is the title of the book. Here **vision** is used in the general sense of a message from Yahweh, rather than to indicate how Obadiah received that message. **Vision** here is a metaphor for the way that God gives knowledge to people. Alternate translation: "The message that God gave to Obadiah" or "The prophecy of Obadiah"
1:1	jdr1		rc://*/ta/man/translate/translate-names	עֹֽבַדְיָ֑ה	1	Some English translations call the prophet Abdias, but Obadiah is the form of his name most commonly used in English. Use the form of the name that is used in your source language or a form that is similar that sounds like a name in your language.
1:1	sv9x		rc://*/ta/man/translate/writing-quotations	כֹּֽה־אָמַר֩ אֲדֹנָ֨⁠י יְהוִ֜ה	1	This introduces the rest of the book as a message from God. Use a form here that is natural in your language for introducing what someone says.
1:1	s7if		rc://*/ta/man/translate/translate-names	יְהוִ֜ה	1	This is the name of God that he revealed to his people in the Old Testament.
"""
parse_translation_notes(translation_notes)

keywords = """
1:1	zwq9	name	עֹֽבַדְיָ֑ה	1	rc://*/tw/dict/bible/names/obadiah
1:1	hjfe	keyterm	אֲדֹנָ֨⁠י	1	rc://*/tw/dict/bible/kt/lord
1:1	vznt	keyterm	יְהוִ֜ה	1	rc://*/tw/dict/bible/kt/yahweh
1:1	h5tb	name	לֶ⁠אֱד֗וֹם	1	rc://*/tw/dict/bible/names/edom
1:1	hhhx	keyterm	יְהוָה֙	1	rc://*/tw/dict/bible/kt/yahweh
1:1	k7s2		וְ⁠צִיר֙	1	rc://*/tw/dict/bible/other/messenger
1:1	es3x		בַּ⁠גּוֹיִ֣ם	1	rc://*/tw/dict/bible/other/nation
"""
parse_keywords(keywords)
