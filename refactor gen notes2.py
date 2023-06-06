import re
import random
import csv
from itertools import product


def get_verse_text(source_file, chapter, verse):
    verse_text = ''
    verse_start = False
    
    for line in source_file:
        if line.startswith('\\c ' + chapter):
            verse_start = True
        elif line.startswith('\\c '):
            verse_start = False
        elif line.startswith('\\v ' + verse) and verse_start:
            verse_text += line[4:].strip()
        elif line.startswith('\\v ') and verse_start:
            break
        elif verse_start:
            # Ignore text within footnotes
            if '\\f' in line:
                line = line[:line.find('\\f')] + line[line.rfind('\\f*')+3:]
            verse_text += line.strip() + ' '
    if int(chapter) < 2:
        print(verse_text)

    return verse_text


def generate_all_alternatives(text):
    components = text.split()
    alternatives = [comp.split('/') for comp in components]
    sentences = [' '.join(combo) for combo in product(*alternatives)]
    return sentences

def choose_alternatives(source1, source2, alternatives):
    source1 = source1.replace("{", "").replace("}", "")
    source2 = source2.replace("{", "").replace("}", "")

    all_alternatives = [generate_all_alternatives(alt) for alt in alternatives]

    valid_alternatives = []
    for alt_set in all_alternatives:
        valid_alt_set = [alt for alt in alt_set if alt not in source1 and alt not in source2]
        if valid_alt_set:
            valid_alternatives.append(valid_alt_set)

    chosen_alternatives = [random.choice(valid_alt_set) for valid_alt_set in valid_alternatives]

    return chosen_alternatives

# Parsing the usfm files
def parse_usfm(file_path):
    with open(file_path, 'r', encoding='utf8') as file:
        data = file.readlines()
    return data

# Read the source files
source_file_1 = parse_usfm('C:\\Users\\benja\\Downloads\\ust\\01-GEN.usfm')
source_file_2 = parse_usfm('C:\\Users\\benja\\Downloads\\ult\\01-GEN.usfm')

# Open the tsv file and read each line
with open('C:\\Users\\benja\\Documents\\uwgit\\en_tn\\tn_GEN.tsv', 'r', encoding='utf8') as tsv_in, open('C:\\Users\\benja\\Downloads\\tn_GEN.tsv', 'w', encoding='utf8', newline='') as tsv_out:
    tsv_reader = csv.reader(tsv_in, delimiter='\t')
    tsv_writer = csv.writer(tsv_out, delimiter='\t')
    
    # Write the headers to the new file
    headers = next(tsv_reader)
    tsv_writer.writerow(headers)
    
    # Initialize the current chapter and verse
    current_chapter = current_verse = ''
    source_text_1 = source_text_2 = ''

    # Process each line
    for row in tsv_reader:
        reference, id_, tags, support_reference, quote, occurrence, note = row
        if reference.startswith('front') or reference.endswith(":intro"):
            tsv_writer.writerow(row)
            continue

        # Update the current chapter and verse based on the reference
        chapter, verse = reference.split(':')
        if chapter != current_chapter:
            # Update the current chapter
            current_chapter = chapter
            source_text_1 = source_text_2 = ''
        if verse != current_verse:
            # Update the current verse
            current_verse = verse
            source_text_1 = get_verse_text(source_file_1, current_chapter, current_verse)
            source_text_2 = get_verse_text(source_file_2, current_chapter, current_verse)

        # Extract the alternates
        alternates = re.findall(r'“([^”]+)”', note)
        alternate_texts = [alt for alt in alternates if ' or ' in alt]

        if not alternate_texts:
            tsv_writer.writerow(row)
            continue

        # Replace the alternates in the note
        for alt in alternate_texts:
            note = note.replace(f'“{alt}”', '')

        # Generate the new alternates
        new_alternates = choose_alternatives(source_text_1, source_text_2, alternate_texts)

        # Append the new alternates to the note
        for new_alt in new_alternates:
            note += ' Alternate translation: '
            note += ' or '.join([f'“{alt}”' for alt in new_alternates])

            # Replace curly quotes with markdown bold in the note
            note = re.sub(r'“([^”]+)”', r'**\1**', note)

            # Write the new line to the file
            new_row = [reference, id_, tags, support_reference, quote, occurrence, note]
            tsv_writer.writerow(new_row)
