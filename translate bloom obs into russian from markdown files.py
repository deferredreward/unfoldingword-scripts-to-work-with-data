import os
import re

def process_files(english_path, russian_path, html_path):
    # Open and read the English and Russian files
    with open(english_path, 'r', encoding='utf-8') as en_file, \
         open(russian_path, 'r', encoding='utf-8') as ru_file:
        en_lines = en_file.readlines()
        ru_lines = ru_file.readlines()

    # Read the HTML file
    with open(html_path, 'r', encoding='utf-8') as html_file:
        html_content = html_file.read()

    # Iterate through the English and Russian lines
    for en_line, ru_line in zip(en_lines, ru_lines):
        en_line = en_line.strip()
        ru_line = ru_line.strip()

        # Check if the line is not an image or title
        if not en_line.startswith("#") and \
           not en_line.startswith("!"):
            # Convert the line to a pattern that matches the corresponding HTML tag
            pattern = re.escape(f"<p>{en_line}</p>")
            replacement = f"<p>{ru_line}</p>"
            html_content = re.sub(pattern, replacement, html_content, count=1)  # Replace only the first occurrence

    # Write the updated content back to the HTML file
    with open(html_path, 'w', encoding='utf-8') as html_file:
        html_file.write(html_content)

if __name__ == "__main__":
    english_dir = "C:\\Users\\benja\\Documents\\GitHub\\en_obs\\content"
    russian_dir = "C:\\Users\\benja\\Downloads\\ru_obs-v9\\ru_obs\\content"
    html_path = "C:\\Users\\benja\\Downloads\\Open Bible Stories.htm"

    # Assuming filenames are the same for corresponding English and Russian files
    for filename in os.listdir(english_dir):
        if filename.endswith(".md"):
            english_path = os.path.join(english_dir, filename)
            russian_path = os.path.join(russian_dir, filename)
            process_files(english_path, russian_path, html_path)
