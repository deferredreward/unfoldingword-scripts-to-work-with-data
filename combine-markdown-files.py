import os
import shutil

def combine_md_files(source_dir, output_dir):
    # Create the output directory if it doesn't exist
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Iterate through all subdirectories in the source directory
    for folder_name in os.listdir(source_dir):
        folder_path = os.path.join(source_dir, folder_name)
        
        # Check if it's a directory
        if os.path.isdir(folder_path):
            combined_content = ""
            
            # List of files to combine in order
            files_to_combine = ['title.md', 'subtitle.md', '01.md']
            
            for file_name in files_to_combine:
                file_path = os.path.join(folder_path, file_name)
                
                # Check if the file exists
                if os.path.exists(file_path):
                    with open(file_path, 'r', encoding='utf-8') as file:
                        combined_content += file.read() + "\n\n"
            
            # If we have any content, write it to a new file
            if combined_content:
                output_file_path = os.path.join(output_dir, f"{folder_name}.md")
                with open(output_file_path, 'w', encoding='utf-8') as output_file:
                    output_file.write(combined_content.strip())
                print(f"Created {output_file_path}")

# Set up the paths
source_directory = r"C:\Users\benja\Documents\GitHub\en_ta\translate"
output_directory = r"C:\Users\benja\Downloads\ta-flat"

# Run the function
combine_md_files(source_directory, output_directory)

print("Process completed.")
