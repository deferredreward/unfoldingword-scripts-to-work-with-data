import re
import traceback

def parse_aligned_usfm(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()

        book = re.search(r'\\id\s+([A-Z]{3})', content)
        book = book.group(1) if book else "Unknown"
        aligned_words = []
        current_chapter = 1
        current_verse = 1

        verses = re.split(r'\\v\s+(\d+)\s*', content)[1:]

        for i in range(0, len(verses), 2):
            current_verse = int(verses[i])
            verse_content = verses[i+1]
            

            zaln_starts = list(re.finditer(r'\\zaln-s\s+\|([^\\]*)', verse_content))
            
            

            for j, start_match in enumerate(zaln_starts):
                try:
                    end_index = verse_content.find('\\zaln-e', start_match.end())
                    if end_index == -1:
                        print(f"Warning: No closing zaln-e found for zaln-s in {book} {current_chapter}:{current_verse}")
                        continue
                    
                    zaln_block = verse_content[start_match.start():end_index + 8]
                    
                    # if current_chapter == 4 and current_verse == 22:
                    #     print("Zaln block: " + zaln_block)                        

                    hebrew_attrs = start_match.group(1)
                    x_content = re.search(r'x-content="([^"]*)"', hebrew_attrs)
                    x_content = x_content.group(1) if x_content else ""

                    h_occurrence = re.search(r'x-occurrence="(\d+)"', hebrew_attrs)
                    h_occurrence = int(h_occurrence.group(1)) if h_occurrence else 1
                    
                    h_occurrences = re.search(r'x-occurrences="(\d+)"', hebrew_attrs)
                    h_occurrences = int(h_occurrences.group(1)) if h_occurrences else 1

                    gl_words = re.finditer(r'\\w\s+([^|\\]*?)\|([^\\]*?)\\w\*', zaln_block)
                    
                    for gl_word_match in gl_words:
                        gl_word = gl_word_match.group(1).strip()
                        # if current_chapter == 4 and current_verse == 22: print (f"GL WORD MATCH: {gl_word_match}")

                        # gl_occurrence = 1
                        # gl_occurrences = 1

                        gl_occurrence = re.search(r'x-occurrence="(\d+)"', gl_word_match.group(0))
                        gl_occurrence = int(gl_occurrence.group(1)) if gl_occurrence else 1
                        
                        gl_occurrences = re.search(r'x-occurrences="(\d+)"', gl_word_match.group(0))
                        gl_occurrences = int(gl_occurrences.group(1)) if gl_occurrences else 1

                        aligned_words.append((book, current_chapter, current_verse, gl_word, gl_occurrence, gl_occurrences, x_content, h_occurrence, h_occurrences))
                        # if current_chapter == 4 and current_verse == 22:
                            # print(book, current_chapter, current_verse, gl_word, gl_occurrence, gl_occurrences, x_content, h_occurrence, h_occurrences)
                            # print()
                
                except Exception as e:
                    print(f"Error processing zaln block in {book} {current_chapter}:{current_verse}")
                    print(f"zaln block content: {zaln_block}")
                    print(f"Error: {str(e)}")

            chapter_match = re.search(r'\\c\s+(\d+)', verse_content)
            if chapter_match:
                current_chapter = int(chapter_match.group(1))

        if not aligned_words:
            print(f"No aligned words found in file: {file_path}")
        else:
            print(f"Found {len(aligned_words)} aligned words in file: {file_path}.")
            # for i, word in enumerate(aligned_words[2770:], 1):
            #     print(f"{i}. {word}")

        return aligned_words

    except Exception as e:
        print(f"Error processing file {file_path}: {str(e)}")
        print("Exception details:")
        print(traceback.format_exc())
        return []