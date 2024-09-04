import os
import re
import shutil
from bs4 import BeautifulSoup

def extract_article_names(html_file):
    with open(html_file, 'r', encoding='utf-8') as file:
        soup = BeautifulSoup(file, 'html.parser')
        
    pattern = r'https://git\.door43\.org/unfoldingWord/en_ta/src/branch/master/translate/(.*?)/01\.md'
    article_names = set()
    
    for link in soup.find_all('a', href=True):
        match = re.search(pattern, link['href'])
        if match:
            article_names.add(match.group(1))
    
    return article_names

def move_unused_articles(ta_flat_dir, used_articles):
    not_used_dir = os.path.join(ta_flat_dir, 'not used')
    if not os.path.exists(not_used_dir):
        os.makedirs(not_used_dir)
    
    for filename in os.listdir(ta_flat_dir):
        if filename.endswith('.md'):
            article_name = filename[:-3]  # Remove '.md' extension
            if article_name not in used_articles:
                src = os.path.join(ta_flat_dir, filename)
                dst = os.path.join(not_used_dir, filename)
                shutil.move(src, dst)
                print(f"Moved {filename} to 'not used' directory")

# Set up the paths
html_file = r"C:\Users\benja\Downloads\ta-articles.htm"
ta_flat_dir = r"C:\Users\benja\Downloads\ta-flat"

# Extract article names from the HTML file
used_articles = extract_article_names(html_file)

# Move unused articles
move_unused_articles(ta_flat_dir, used_articles)

print("Process completed.")
