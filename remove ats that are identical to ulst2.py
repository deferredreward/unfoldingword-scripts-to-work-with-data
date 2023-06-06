import re
import random
from itertools import product

def generate_all_alternatives(text):
    components = text.split()

    # For each component, split by '/' to create a list of alternatives
    alternatives = [comp.split('/') for comp in components]

    # Generate all possible combinations of alternatives
    sentences = [' '.join(combo) for combo in product(*alternatives)]
    return sentences

def choose_alternatives(source1, source2, alternatives):
    source1 = source1.replace("{", "").replace("}", "")
    source2 = source2.replace("{", "").replace("}", "")

    all_alternatives = []
    for alt in alternatives:
        all_alternatives.append(generate_all_alternatives(alt))

    valid_alternatives = []
    for alt_set in all_alternatives:
        valid_alt_set = []
        for alt in alt_set:
            if alt not in source1 and alt not in source2:
                valid_alt_set.append(alt)
        if valid_alt_set:
            valid_alternatives.append(valid_alt_set)

    chosen_alternatives = []
    for valid_alt_set in valid_alternatives:
        alt = random.choice(valid_alt_set)
        chosen_alternatives.append(alt)

    return chosen_alternatives

source_text_1 = "Then Lot went out and spoke to his sons-in-law who were to take his daughters, and he said, “Get up, get out of this place, because Yahweh is destroying the city!” But it seemed like he was joking in the eyes of his sons-in-law."
source_text_2 = "So Lot went to his {future} sons-in-law who were engaged to his daughters, and he warned them, “Hurry up {and} leave this city, because Yahweh is about to destroy it!” But his sons-in-law thought that he was joking, {so they ignored him}."
alternate_texts = ["But his sons-in-law thought that he was joking, so they ignored him." , "But his sons-in-law did not listen to him, because they thought he was joking."]

result = choose_alternatives(source_text_1, source_text_2, alternate_texts)
for alt in result:
    print(alt)
