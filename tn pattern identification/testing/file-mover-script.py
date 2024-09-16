import os
import shutil
import re

# List of published books with their abbreviations
PUBLISHED_BOOKS = [
    "GEN", "EXO", "RUT", "EZR", "NEH", "EST", "JOB", "PRO", "SNG", "OBA", "JON", "ZEP", "HAG",
    "MAT", "MRK", "LUK", "JHN", "ACT", "ROM", "1CO", "2CO", "GAL", "EPH", "PHP", "COL",
    "1TH", "2TH", "1TI", "2TI", "TIT", "PHM", "HEB", "JAS", "1PE", "2PE", "1JN", "2JN", "3JN", "JUD", "REV"
]

def extract_book_code(filename):
    # Match three capital letters or a number followed by two capital letters
    match = re.search(r'(?<!\w)([1-3]?[A-Z]{2,3})(?!\w)', filename)
    return match.group(1) if match else None

def is_published(book_code):
    return book_code in PUBLISHED_BOOKS or book_code[1:] in PUBLISHED_BOOKS

def move_file(source_path, dest_path):
    try:
        shutil.move(source_path, dest_path)
        print(f"Moved {os.path.basename(source_path)} to {os.path.dirname(dest_path)}")
        return True
    except shutil.Error as e:
        print(f"Error moving {os.path.basename(source_path)}: {e}")
        return False

def process_directory(directory, target_book_code, action):
    published_dir = os.path.join(directory, "published")
    not_published_dir = os.path.join(directory, "not published")
    os.makedirs(published_dir, exist_ok=True)
    os.makedirs(not_published_dir, exist_ok=True)

    for filename in os.listdir(directory):
        book_code = extract_book_code(filename)
        if book_code and (book_code == target_book_code or book_code[1:] == target_book_code):
            source_path = os.path.join(directory, filename)
            if os.path.isfile(source_path):
                if action == "in":
                    dest_dir = published_dir if is_published(book_code) else not_published_dir
                else:  # action == "out"
                    dest_dir = directory
                dest_path = os.path.join(dest_dir, filename)
                move_file(source_path, dest_path)

def move_other_books(directory, selected_book):
    published_dir = os.path.join(directory, "published")
    not_published_dir = os.path.join(directory, "not published")
    os.makedirs(published_dir, exist_ok=True)
    os.makedirs(not_published_dir, exist_ok=True)

    for filename in os.listdir(directory):
        source_path = os.path.join(directory, filename)
        if os.path.isfile(source_path):
            book_code = extract_book_code(filename)
            if book_code and book_code != selected_book and book_code[1:] != selected_book:
                if is_published(book_code):
                    dest_path = os.path.join(published_dir, filename)
                else:
                    dest_path = os.path.join(not_published_dir, filename)
                if move_file(source_path, dest_path):
                    print(f"Moved {book_code} files to {'published' if is_published(book_code) else 'not published'} directory")

def main():
    print("Welcome to the File Mover Script!")
    print("Options:")
    print("(p) - All published books")
    print("(u) - All unpublished books")
    print("(a) - All books")
    print("Or enter a three-letter book code (e.g., RUT, OBA, 1JN)")

    choice = input("Enter your choice: ").strip().upper()

    if choice == "P":
        books = PUBLISHED_BOOKS
    elif choice == "U":
        books = [book for book in os.listdir("./data") if extract_book_code(book) and not is_published(extract_book_code(book))]
    elif choice == "A":
        books = [book for book in os.listdir("./data") if extract_book_code(book)]
    elif len(choice) in [3, 4] and extract_book_code(choice):
        books = [choice]
    else:
        print("Invalid choice. Please run the script again.")
        return

    action = input("Move files (i)n or (o)ut of the published/not published directories? ").strip().lower()
    if action not in ["i", "o"]:
        print("Invalid action. Please run the script again.")
        return

    action = "in" if action == "i" else "out"

    for book in books:
        for directory in os.listdir("./data"):
            dir_path = os.path.join("./data", directory)
            if os.path.isdir(dir_path):
                process_directory(dir_path, book, action)

    if len(books) == 1:
        move_others = input("Do you want to move other books back to their appropriate directories? (Y/n): ").strip().lower()
        if move_others == '' or move_others == 'y':
            for directory in os.listdir("./data"):
                dir_path = os.path.join("./data", directory)
                if os.path.isdir(dir_path):
                    move_other_books(dir_path, books[0])

    print("File moving process completed!")

if __name__ == "__main__":
    main()
