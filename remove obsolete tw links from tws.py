import os
import re

# Define the path to the directory and the file containing obsolete articles.
base_dir = r'C:\Users\benja\Documents\GitHub\en_tw\bible'
obsolete_file_path = r'C:\Users\benja\Documents\GitHub\unfoldingword-scripts-to-work-with-data\twltodelete.txt'  # Replace with your actual path.

# Read obsolete articles into a set for faster lookups.
with open(obsolete_file_path, 'r') as file:
    obsolete_articles = {line.strip() for line in file.readlines()}

def process_file(file_path):
    # Read the content of the file.
    with open(file_path, 'r', encoding="utf-8") as file:
        content = file.readlines()

    # Check and update each line in the content.
    updated_content = []
    for line in content:
        # If the line starts with "(See also:", we will process it.
        if line.strip().startswith("(See also:"):
            # Find all markdown links in the line.
            links = re.findall(r'\[([^\]]+)\]\(([^)]+)\)', line)
            for name, url in links:
                # If the link name exists in the set of obsolete articles, we remove it.
                if name in obsolete_articles:
                    line = line.replace(f'[{name}]({url})', '').replace(', ,', ',')
            # Remove trailing comma before the closing parenthesis.
            line = line.replace(', )', ' )')
            # If after processing, the line only has "(See also: )", we skip it.
            if line.strip() != "(See also: )":
                updated_content.append(line)
        else:
            updated_content.append(line)

    # Write the updated content back to the file.
    with open(file_path, 'w', encoding="utf-8") as file:
        file.writelines(updated_content)

# Iterate over all subdirectories and files.
for subdir, _, files in os.walk(base_dir):
    for file in files:
        if file.endswith('.md'):
            process_file(os.path.join(subdir, file))

print("Processing complete!")
