import random
import string
import re

def generate_valid_id():
    # First character must be a-z
    first = random.choice(string.ascii_lowercase)
    # Rest can be a-z or 0-9
    rest = ''.join(random.choices(string.ascii_lowercase + string.digits, k=3))
    return first + rest

def is_valid_id(id_str):
    # Check if ID matches pattern: first char a-z, followed by 3 chars that are a-z or 0-9
    pattern = r'^[a-z][a-z0-9]{3}$'
    return bool(re.match(pattern, id_str))

# Set to store used IDs to ensure uniqueness
used_ids = set()

# Read input file and process lines
with open('tn_LEV.tsv', 'r', encoding='utf-8') as infile:
    lines = infile.readlines()

# Process each line
new_lines = []
for line in lines:
    if line.strip():  # Skip empty lines
        parts = line.split('\t')
        if len(parts) > 2:  # Make sure we have enough columns
            current_id = parts[1]
            
            # If ID is invalid or already used, generate new one
            while not is_valid_id(current_id) or current_id in used_ids:
                current_id = generate_valid_id()
                # Prevent infinite loop if we somehow run out of IDs
                if len(used_ids) >= 26 * 36 * 36 * 36:
                    raise Exception("Ran out of unique IDs!")
            
            used_ids.add(current_id)
            parts[1] = current_id
            new_line = '\t'.join(parts)
        else:
            new_line = line
        new_lines.append(new_line)
    else:
        new_lines.append(line)

# Write output file
with open('tn_LEVid.tsv', 'w', encoding='utf-8') as outfile:
    outfile.writelines(new_lines) 