import config, os, traceback
from parsers.usfm_parser import parse_usfm_file
from parsers.aligned_usfm_parser import parse_aligned_usfm
from parsers.twl_operations import process_twl_files
from db_operations.bible_verse_operations import insert_bible_verses, insert_word_alignments
from db_operations.aligned_verse_operations import insert_aligned_data
from utils.file_utils import get_usfm_files, count_usfm_files
from db_operations.db_functions import prepare_db

def process_origL_usfm_files(directory, db_path):
    all_verses = []
    total_files = count_usfm_files(directory)
    print(f"Processing {total_files} USFM files from {directory}")
    
    for file_path in get_usfm_files(directory):
        try:
            verses = parse_usfm_file(file_path)
            all_verses.extend(verses)
            print(f"Processed {file_path}")
        except Exception as e:
            print(f"Error processing file {file_path}: {str(e)}")
    
    if all_verses:
        bible_verse_ids = insert_bible_verses(all_verses, db_path, clear_table=True)
        return bible_verse_ids
    return []

def process_aligned_usfm_files(directory, db_path, clear_tables=False):
    all_aligned_words = []
    all_alignment_data = []
    for filename in os.listdir(directory):
        if filename.endswith('.usfm'):
            file_path = os.path.join(directory, filename)
            try:
                # aligned_words, alignment_data = parse_aligned_usfm(file_path)
                aligned_words = parse_aligned_usfm(file_path)
                all_aligned_words.extend(aligned_words)
                # all_alignment_data.extend(alignment_data)
                print(f"Processed {filename}: Found {len(aligned_words)} aligned words")
            except Exception as e:
                print(f"Error processing aligned file {filename}: {str(e)}")
                print("Exception details:")
                print(traceback.format_exc())

    if all_aligned_words:
        # insert_aligned_data(all_aligned_words, all_alignment_data, db_path, clear_tables)
        insert_aligned_data(all_aligned_words, db_path, clear_tables)

    else:
        print("No aligned verses were parsed. Check the USFM files and error messages.")

def main(create_new_database=True, clear_tables=False):
    if create_new_database:
        db_path = prepare_db()
    else:
        db_path = prepare_db(config.DB_PATH)


    # bible_verse_ids = process_origL_usfm_files(config.ORIGL_USFM_DIRECTORY, db_path)
    # process_aligned_usfm_files(config.ALIGNED_USFM_DIRECTORY, db_path, clear_tables)

    process_twl_files(config.TWL_DIRECTORY, db_path)

    print("Script execution completed.")

if __name__ == "__main__":
    main(create_new_database=False, clear_tables=False)  # Set clear_tables to False if you don't want to clear tables