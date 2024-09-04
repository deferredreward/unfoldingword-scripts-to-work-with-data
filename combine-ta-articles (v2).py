import os

def combine_ta_articles(input_dir, output_file):
    with open(output_file, 'w', encoding='utf-8') as outfile:
        first_file = True
        for filename in sorted(os.listdir(input_dir)):
            if filename.endswith('.md') and filename != 'ta-articles-for-notes.md':
                file_path = os.path.join(input_dir, filename)
                
                # Add horizontal line between files, except before the first file
                if not first_file:
                    outfile.write('\n\n---\n\n')
                else:
                    first_file = False
                
                # Write the filename
                outfile.write(f"File: {filename}\n\n")
                
                with open(file_path, 'r', encoding='utf-8') as infile:
                    # Read the entire content of the file
                    content = infile.read().strip()
                    
                    # Split the content into lines
                    lines = content.split('\n')
                    
                    # Convert the first line to an H1 header if it's not already
                    if lines and not lines[0].startswith('# '):
                        lines[0] = '# ' + lines[0]
                    
                    # Write the modified content to the output file
                    outfile.write('\n'.join(lines))
                
                print(f"Added content from {filename}")

# Set up the paths
input_directory = r"C:\Users\benja\Downloads\ta-flat"
output_file = os.path.join(input_directory, "ta-articles-for-notes.md")

# Run the function
combine_ta_articles(input_directory, output_file)

print("Process completed. Combined file created:", output_file)
