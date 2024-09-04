import os
from collections import defaultdict

def group_files_recursive(directory):
    groups = defaultdict(list)
    base_files = set()

    for root, _, files in os.walk(directory):
        for file in files:
            full_path = os.path.join(root, file)
            rel_path = os.path.relpath(full_path, directory)
            
            if '-' in file:
                base = file.split('-')[0]
                groups[base].append(rel_path)
            else:
                base_files.add(file.split('.')[0])

    output = []
    for base, files in groups.items():
        group_output = []
        base_file = f"{base}.md"
        if any(f.endswith(base_file) for f in files):
            group_output.append(next(f for f in files if f.endswith(base_file)))
        elif base in base_files:
            group_output.append(f"{base}.md (in root)")
        else:
            group_output.append(f"[Missing: {base}.md]")
        
        group_output.extend(sorted(f for f in files if not f.endswith(base_file)))
        output.append('\n'.join(group_output))

    return '\n\n'.join(output)

# Directory path
directory = r"C:\Users\benja\Documents\GitHub\en_tw\bible"

# Generate the output
result = group_files_recursive(directory)

# Print to terminal
print(result)

# Write to file in the script directory
script_dir = os.path.dirname(os.path.abspath(__file__))
output_file = os.path.join(script_dir, 'grouped_files_recursive.txt')

with open(output_file, 'w') as f:
    f.write(result)

print(f"\nOutput has been written to: {output_file}")
