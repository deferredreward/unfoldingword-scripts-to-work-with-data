import os
import re

HTML_PATH = 'C:\\Users\\benja\\Downloads\\Open Bible Stories.htm'
EN_DIR = 'C:\\Users\\benja\\Documents\\GitHub\\en_obs\\content'
RU_DIR = 'C:\\Users\\benja\\Downloads\\ru_obs-v9\\ru_obs\\content'
en_ru_mapping = {}
missing_lines = []

def get_partial_match_key(p_content, en_ru_map):
    # First, try for a full match.
    if p_content in en_ru_map:
        return p_content
    # If full match fails, then look for startswith match.
    matching_keys = [key for key in en_ru_map if key.startswith(p_content)]
    if matching_keys:
        # Return the longest matching key (to get the most specific match)
        return max(matching_keys, key=len)
    missing_lines.append(p_content)
    return None

# Read the English and Russian contents and populate the en_ru_mapping dictionary
for filename in os.listdir(EN_DIR):
    if filename.endswith('.md'):
        with open(os.path.join(EN_DIR, filename), 'r', encoding='utf-8') as en_file, \
             open(os.path.join(RU_DIR, filename), 'r', encoding='utf-8') as ru_file:

            # Drop blank lines and strip trailing/leading spaces and specific characters
            en_lines = [line.strip().lstrip('# ').strip('_') for line in en_file.readlines() if line.strip()]
            ru_lines = [line.strip().lstrip('# ').strip('_') for line in ru_file.readlines() if line.strip()]

            for en_line, ru_line in zip(en_lines, ru_lines):
                en_ru_mapping[en_line] = ru_line

# Process the HTML file
with open(HTML_PATH, 'r', encoding='utf-8') as html_file:
    html_content = html_file.read()
    p_matches = re.findall(r'<p>(.*?)</p>', html_content)
    p_matches = [p for p in p_matches if p.strip()]  # Filter out blank matches

    for p_content in p_matches:
        matching_key = get_partial_match_key(p_content, en_ru_mapping)
        if matching_key:
            html_content = html_content.replace(f'<p>{p_content}</p>', f'<p>{en_ru_mapping[matching_key]}</p>', 1)

with open(HTML_PATH.replace('.htm', '-translated.htm'), 'w', encoding='utf-8') as out_file:
    out_file.write(html_content)

# Write missing lines to missing.txt
with open('C:\\Users\\benja\\Downloads\\missing.txt', 'w', encoding='utf-8') as missing_file:
    missing_file.write('\n'.join(missing_lines))
