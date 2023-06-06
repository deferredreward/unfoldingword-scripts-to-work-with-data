import re
from itertools import product

def generate_sentences(text):
    # Split text into components separated by spaces
    components = text.split()

    # For each component, split by '/' to create a list of alternatives
    alternatives = [comp.split('/') for comp in components]

    # Generate all possible combinations of alternatives
    sentences = [' '.join(combo) for combo in product(*alternatives)]
   
    return sentences

text = "Then God/he separated/divided the light from the darkness so that each had its own time."
sentences = generate_sentences(text)
for sentence in sentences:
    print(sentence)
