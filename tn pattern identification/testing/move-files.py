import os
import shutil

# List of published books
published_books = ['GEN', 'EXO', 'RUT', 'EZR', 'NEH', 'EST', 'JOB', 'PRO', 'SNG', 'OBA', 'JON', 'ZEP', 'HAG', 'MAT', 'MRK', 'LUK', 'JHN', 'ACT', 'ROM', '1CO', '2CO', 'GAL', 'EPH', 'PHP', 'COL', '1TH', '2TH', '1TI', '2TI', 'TIT', 'PHM', 'HEB', 'JAS', '1PE', '2PE', '1JN', '2JN', '3JN', 'JUD', 'REV']

def move_files(book_code=None, move_published=True, move_unpublished=True, move_into_dirs=True):
    # Base directory
    base_dir = './data'
    
    # Traverse through each directory under './data'
    for dir_name in os.listdir(base_dir):
        dir_path = os.path.join(base_dir, dir_name)
        
        if os.path.isdir(dir_path):
            pub_dir = os.path.join(dir_path, 'published')
            unpub_dir = os.path.join(dir_path, 'not published')

            # Ensure published and not published directories exist
            if not os.path.exists(pub_dir):
                os.makedirs(pub_dir)
            if not os.path.exists(unpub_dir):
                os.makedirs(unpub_dir)

            # Traverse files in the base directory
            for filename in os.listdir(dir_path):
                if os.path.isfile(os.path.join(dir_path, filename)) and (book_code is None or book_code in filename):
                    target_dir = None
                    if any(b in filename for b in published_books):
                        if move_published:
                            target_dir = pub_dir if move_into_dirs else dir_path
                    else:
                        if move_unpublished:
                            target_dir = unpub_dir if move_into_dirs else dir_path

                    if target_dir:
                        shutil.move(os.path.join(dir_path, filename), os.path.join(target_dir, filename))

def sort_remaining_files():
    # Base directory
    base_dir = './data'
    
    for dir_name in os.listdir(base_dir):
        dir_path = os.path.join(base_dir, dir_name)
        
        if os.path.isdir(dir_path):
            pub_dir = os.path.join(dir_path, 'published')
            unpub_dir = os.path.join(dir_path, 'not published')

            # Ensure published and not published directories exist
            if not os.path.exists(pub_dir):
                os.makedirs(pub_dir)
            if not os.path.exists(unpub_dir):
                os.makedirs(unpub_dir)

            # Sort remaining files
            for filename in os.listdir(dir_path):
                if os.path.isfile(os.path.join(dir_path, filename)):
                    if any(b in filename for b in published_books):
                        shutil.move(os.path.join(dir_path, filename), os.path.join(pub_dir, filename))
                    else:
                        shutil.move(os.path.join(dir_path, filename), os.path.join(unpub_dir, filename))

def main():
    while True:
        # Ask user what to do
        choice = input("Do you want to move (p)ublished, (u)npublished, (a)ll or specify a three-letter book code (e.g., RUT)? ")
        move_into_dirs = input("Do you want to move the files into their published/unpublished directories or out for active work? (in/out): ").lower() == 'in'

        if choice == 'p':
            print("Moving all published books.")
            move_files(move_published=True, move_unpublished=False, move_into_dirs=move_into_dirs)
        elif choice == 'u':
            print("Moving all unpublished books.")
            move_files(move_published=False, move_unpublished=True, move_into_dirs=move_into_dirs)
        elif choice == 'a':
            print("Moving all books.")
            move_files(move_published=True, move_unpublished=True, move_into_dirs=move_into_dirs)
        elif len(choice) == 3:
            print(f"Moving files for the book: {choice.upper()}")
            move_files(book_code=choice.upper(), move_into_dirs=move_into_dirs)
        else:
            print("Invalid input, please try again.")
        
        # Ask if the user wants to sort remaining files
        sort_others = input("Do you want to sort the remaining files into their directories? (y/n): ").lower()
        if sort_others == 'y':
            sort_remaining_files()
        
        # Continue or not
        cont = input("Do you want to continue (y/n)? ")
        if cont.lower() != 'y':
            break

if __name__ == "__main__":
    main()
