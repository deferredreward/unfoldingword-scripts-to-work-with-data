import csv
import sys
import os

def process_tsv(file_path):
    # The output file name will be the original file name with "-activated" added before the file extension.
    output_file_path = os.path.splitext(file_path)[0] + "-activated.tsv"
    
    # Open the TSV file for reading and the new file for writing.
    with open(file_path, 'r', newline='', encoding='utf-8') as infile, \
         open(output_file_path, 'w', newline='', encoding='utf-8') as outfile:
        
        reader = csv.reader(infile, delimiter='\t')
        writer = csv.writer(outfile, delimiter='\t')

        # Write the header (first row) to the output file.
        header = next(reader)
        writer.writerow(header)

        # Process each row in the TSV.
        for row in reader:
            # If there's anything in the 5th field (index 4), change the 6th field (index 5) from 0 to 1.
            if row[4]:
                row[5] = '1'
            writer.writerow(row)

if __name__ == "__main__":
    # Check if a file is passed as an argument.
    if len(sys.argv) > 1:
        process_tsv(sys.argv[1])
    else:
        print("Please drag and drop a TSV file onto the script.")

