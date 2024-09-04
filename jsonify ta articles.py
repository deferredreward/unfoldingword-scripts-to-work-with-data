import re
import json
import os

def parse_content(content):
    # Split content into sections by file marker
    sections = re.split(r'---+', content)
    result = {}

    for section in sections:
        if section.strip():
            # Extract the file identifier
            file_match = re.match(r'File:\s*(\S+)', section)
            if file_match:
                file_id = file_match.group(1)
                result[file_id] = {}
                # Extract title
                title_match = re.search(r'#\s*(.*)', section)
                if title_match:
                    result[file_id]['title'] = title_match.group(1).strip()

                # Extract sections like "Description", "Reason This Is a Translation Issue", etc.
                current_section = None
                for line in section.splitlines():
                    line = line.strip()
                    if line.startswith('#'):
                        continue
                    if line.startswith('### '):
                        current_section = line[4:].lower().replace(' ', '_')
                        result[file_id][current_section] = ""
                    elif current_section:
                        if line.startswith('> '):
                            # Handle block quotes separately
                            if 'bible_examples' not in result[file_id]:
                                result[file_id]['bible_examples'] = []
                            result[file_id]['bible_examples'].append({"text": line[2:], "explanation": ""})
                        elif line.startswith('> > '):
                            # Add explanation to the last example
                            if result[file_id]['bible_examples']:
                                result[file_id]['bible_examples'][-1]['explanation'] = line[4:]
                        elif line.startswith('*'):
                            # Handle bullet points
                            if 'translation_strategies' not in result[file_id]:
                                result[file_id]['translation_strategies'] = []
                            result[file_id]['translation_strategies'].append({"strategy": line[2:], "example": "", "example-using-strategy": ""})
                        elif line.startswith('(1)'):
                            # Handle numbered strategies
                            if 'translation_strategies' not in result[file_id]:
                                result[file_id]['translation_strategies'] = []
                            result[file_id]['translation_strategies'].append({"strategy": line, "example": "", "example-using-strategy": ""})
                        else:
                            # Add regular text to the current section
                            result[file_id][current_section] += line + " "
    
    # Clean up whitespace in values
    for key in result:
        for section in result[key]:
            if isinstance(result[key][section], str):
                result[key][section] = result[key][section].strip()
            elif isinstance(result[key][section], list):
                for item in result[key][section]:
                    for subkey in item:
                        item[subkey] = item[subkey].strip()
    
    return result



# Define the file path
file_name = "ta-articles-for-notes.md"
file_path = os.path.join(os.path.dirname(__file__), file_name)

# Read the content from the Markdown file
with open(file_path, 'r', encoding='utf-8') as md_file:
    content = md_file.read()


parsed_result = parse_content(content)
file_name = "ta-articles-for-notes.json"
file_path = os.path.join(os.path.dirname(__file__), file_name)

with open(file_path, 'w', encoding='utf-8') as json_file:
    json_file.write(json.dumps(parsed_result, indent=2))
