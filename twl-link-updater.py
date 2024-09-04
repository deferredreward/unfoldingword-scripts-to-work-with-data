import os
import re
import json
from collections import defaultdict

def find_files_with_hyphen(directory):
    groups = defaultdict(list)
    for root, _, files in os.walk(directory):
        for file in files:
            if '-' in file and file.endswith('.md'):
                base = file.split('-')[0]
                relative_path = os.path.relpath(root, directory)
                groups[base].append((os.path.join(relative_path, file), file))
    return groups

def read_ult_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()
    chapters = re.split(r'\\c\s+(\d+)', content)[1:]
    verses = {}
    for i in range(0, len(chapters), 2):
        chapter = int(chapters[i])
        chapter_content = chapters[i+1]
        chapter_verses = re.findall(r'\\v\s+(\d+)\s+(.*?)(?=\\v|\Z)', chapter_content, re.DOTALL)
        verses[chapter] = {int(v): clean_usfm(t.strip()) for v, t in chapter_verses}
    return verses

def clean_usfm(text):
    text = re.sub(r'\\[^\s]+\s+', '', text)
    text = re.sub(r'\s+', ' ', text)
    return text.strip()

def read_twl_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return [line.strip().split('\t') for line in file if line.strip()]

def write_twl_file(file_path, content):
    with open(file_path, 'w', encoding='utf-8') as file:
        for line in content:
            file.write('\t'.join(line) + '\n')

def get_verse_text(ult_verses, chapter, verse):
    try:
        return ult_verses[int(chapter)][int(verse)]
    except KeyError:
        return "Verse not found"


def get_first_usage(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
            match = re.search(r'#\s*(.+)', content)
            if match:
                return match.group(1)
    except FileNotFoundError:
        print(f"Warning: File not found: {file_path}")
    except Exception as e:
        print(f"Error reading file {file_path}: {str(e)}")
    return ""


def get_distinguishing_fact(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()
        facts_section = re.search(r'# Facts:\s*\n(.*?)\n\n', content, re.DOTALL)
        if facts_section:
            facts = facts_section.group(1)
            used_in_sense = re.search(r'used in (?:the )?sense of(.*)', facts)
            if used_in_sense:
                return used_in_sense.group(1).strip()
    return ""

def update_twl_link(twl_dir, ult_dir, output_dir, tw_dir, groups, progress):
    for topic, files in groups.items():
        if topic in progress['completed_topics']:
            print(f"Skipping completed topic: {topic}")
            continue
        print(f"\nProcessing topic: {topic}")
        
        # Show distinguishing fact for the group
        topic_file = next((f for f in files if f[1] == f"{topic}.md"), None)
        if topic_file:
            distinguishing_fact = get_distinguishing_fact(os.path.join(tw_dir, topic_file[0], topic_file[1]))
            if distinguishing_fact:
                print(f"Note: {distinguishing_fact}\n")
        
        for twl_file in os.listdir(output_dir):
            if not twl_file.startswith('twl_') or not twl_file.endswith('.tsv'):
                continue
            
            book = twl_file[4:-4].upper()
            if progress['current_topic'] == topic and progress['current_book'] > book:
                print(f"Skipping completed book: {book}")
                continue
            
            twl_path = os.path.join(output_dir, twl_file)
            if not os.path.exists(twl_path):
                twl_path = os.path.join(twl_dir, twl_file)
            ult_path = next((os.path.join(ult_dir, f) for f in os.listdir(ult_dir) if f.endswith(f'-{book}.usfm')), None)
            
            if not ult_path:
                print(f"Skipping {book}, ULT file not found")
                continue
            
            twl_content = read_twl_file(twl_path)
            ult_verses = read_ult_file(ult_path)
            
            new_twl_content = []
            for line_index, line in enumerate(twl_content):
                if progress['current_topic'] == topic and progress['current_book'] == book and line_index < progress['current_line']:
                    new_twl_content.append(line)
                    continue
                
                if len(line) < 6 or not any(line[5].endswith(f"/tw/dict/bible/other/{f.split('-')[0]}") for f in [file[1] for file in files]):
                    new_twl_content.append(line)
                    continue
                
                verse = f"{book} {line[0]}"
                chapter, verse_num = map(int, line[0].split(':'))
                
                print(f"\n{verse} has a link to '{topic}'.")
                print(f"{int(verse_num)-1}: {get_verse_text(ult_verses, chapter, verse_num-1)}")
                print(f"{verse_num}: {get_verse_text(ult_verses, chapter, verse_num)}")
                print(f"{int(verse_num)+1}: {get_verse_text(ult_verses, chapter, verse_num+1)}")
                
                options = [topic] + [f.split('.')[0] for f in [file[1] for file in files] if f != f"{topic}.md"]
                parent_exists = any(f[1] == f"{topic}.md" for f in files)
                
                if not parent_exists:
                    print(f"The article '{topic}' no longer exists.")
                
                for i, option in enumerate(options, 1):
                    # Find the correct file for this option
                    file_info = next((f for f in files if f[1].startswith(option)), None)
                    print(file_info)
                    if file_info:
                        # Construct the file path correctly
                        file_path = os.path.join(tw_dir, file_info[0])
                        print(f"Debug: Constructed file path: {file_path}")
                        first_usage = get_first_usage(file_path)
                    else:
                        first_usage = ""
                    print(f"({i}) {option} ({first_usage})")

                print(f"({len(options)+1}) deleted")
                print("(q) quit")
                
                while True:
                    choice = input("Enter your choice: ").lower()
                    if choice == 'q':
                        progress['current_topic'] = topic
                        progress['current_book'] = book
                        progress['current_line'] = line_index
                        save_progress(progress)
                        print("Progress saved. Exiting...")
                        return False
                    try:
                        choice = int(choice)
                        if 1 <= choice <= len(options) + 1:
                            break
                        else:
                            print("Invalid choice. Please try again.")
                    except ValueError:
                        print("Invalid input. Please enter a number or 'q' to quit.")
                
                if choice == len(options) + 1:
                    new_twl_content.append(line)
                    continue
                else:
                    chosen_option = options[choice-1]
                    chosen_file = next((f for f in files if f[1].startswith(chosen_option)), files[0])
                    new_link = f"rc://*/tw/dict/bible/{chosen_file[0]}/{chosen_option}"
                    line[5] = new_link
                    new_twl_content.append(line)
                
                # Save progress after each link update
                progress['current_topic'] = topic
                progress['current_book'] = book
                progress['current_line'] = line_index + 1
                save_progress(progress)
            
            output_path = os.path.join(output_dir, twl_file)
            write_twl_file(output_path, new_twl_content)
            print(f"Updated TWL file written to {output_path}")
        
        progress['completed_topics'].append(topic)
        progress['current_book'] = ''
        progress['current_line'] = 0
        save_progress(progress)
    
    return True

def save_progress(progress):
    with open('progress.json', 'w') as f:
        json.dump(progress, f)

def load_progress():
    if os.path.exists('progress.json'):
        with open('progress.json', 'r') as f:
            progress = json.load(f)
    else:
        progress = {}
    
    # Ensure all necessary keys are present
    default_progress = {
        'completed_topics': [],
        'current_topic': '',
        'current_book': '',
        'current_line': 0
    }
    
    for key, value in default_progress.items():
        if key not in progress:
            progress[key] = value
    
    return progress

def main():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    twl_dir = r"C:\Users\benja\Documents\GitHub\en_twl"
    ult_dir = r"C:\Users\benja\Downloads\en_ult"
    tw_dir = r"C:\Users\benja\Documents\GitHub\en_tw\bible"
    output_dir = os.path.join(script_dir, "newTWLs")
    os.makedirs(output_dir, exist_ok=True)

    progress = load_progress()
    
    if progress['current_topic'] or progress['completed_topics']:
        resume = input(f"Do you want to resume from {progress['current_topic'] or 'the beginning'}? (y/n): ").lower() == 'y'
        if not resume:
            progress = {'completed_topics': [], 'current_topic': '', 'current_book': '', 'current_line': 0}
    else:
        print("Starting a new session.")

    groups = find_files_with_hyphen(tw_dir)
    completed = update_twl_link(twl_dir, ult_dir, output_dir, tw_dir, groups, progress)

    if completed:
        print("All topics have been processed.")
        if os.path.exists('progress.json'):
            os.remove('progress.json')

if __name__ == "__main__":
    main()
