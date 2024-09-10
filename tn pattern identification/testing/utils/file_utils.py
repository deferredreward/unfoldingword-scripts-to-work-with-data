# utils/file_utils.py

import os

def get_usfm_files(directory):
    """
    Generator function to yield paths of all USFM files in the given directory.
    
    Args:
    directory (str): Path to the directory containing USFM files.
    
    Yields:
    str: Full path to each USFM file.
    """
    for filename in os.listdir(directory):
        if filename.endswith('.usfm'):
            yield os.path.join(directory, filename)

def count_usfm_files(directory):
    """
    Count the number of USFM files in the given directory.
    
    Args:
    directory (str): Path to the directory containing USFM files.
    
    Returns:
    int: Number of USFM files in the directory.
    """
    return sum(1 for _ in get_usfm_files(directory))

def get_usfm_file_names(directory):
    """
    Get a list of names of all USFM files in the given directory.
    
    Args:
    directory (str): Path to the directory containing USFM files.
    
    Returns:
    list: List of USFM file names (without full path).
    """
    return [os.path.basename(file_path) for file_path in get_usfm_files(directory)]