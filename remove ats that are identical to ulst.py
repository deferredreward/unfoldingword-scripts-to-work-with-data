import re
import random
from itertools import product

def generate_all_alternatives(text):
    components = text.split()

    # For each component, split by '/' to create a list of alternatives
    alternatives = [comp.split('/') for comp in components]

    # Generate all possible combinations of alternatives
    sentences = [' '.join(combo) for combo in product(*alternatives)]
   # print(sentences)
    return sentences

def choose_alternatives(source1, source2, alternatives):
    source1 = source1.replace("{", "").replace("}", "")
    source2 = source2.replace("{", "").replace("}", "")

    all_alternatives = []
    for alt in alternatives:
        all_alternatives.extend(generate_all_alternatives(alt))

    print('\nall: ')
    print(all_alternatives)
    print(len(all_alternatives))

    valid_alternatives = [alt for alt in all_alternatives if alt not in [source1, source2]]

    print('\nvalid: ')
    print(valid_alternatives)
    print(len(valid_alternatives))

    chosen_alternatives = []
    while valid_alternatives and len(chosen_alternatives) < len(alternatives):
        alt = random.choice(valid_alternatives)
        if alt not in chosen_alternatives:
            chosen_alternatives.append(alt)
        valid_alternatives.remove(alt)
    #return valid_alternatives
    print('\n')
    return chosen_alternatives

# source_text_1 = "Then when the dawn came, the angels urged Lot, saying, “Get up, take your wife and your two daughters who are here, so that you are not swept away in the punishment of the city."
# source_text_2 = "Early the next morning, the {two} angels urged Lot, “Hurry up {and} take your wife and your two daughters {out of the city} so that you will not die when {God} punishes {the people of} the city."
# alternate_texts = ["the two angels/messengers urged Lot,", "the/Yahweh’s two angels/messengers urgently told Lot,"]
source_text_1 = "And God saw the light, that {it was} good. Then God separated between the light and the darkness."
source_text_2 = "God observed that the light {was} excellent. Then he divided the light from the darkness {so that each had its own time}."
alternate_texts = ["Then God/he separated/divided the light from the darkness so that each had its own time.",
                   "Then God/he caused the light to have its own time and the darkness to have its own time.",
                   "Then God/he separated the light from the darkness so that it would be light for a number of hours, and then dark for a number of hours."]



result = choose_alternatives(source_text_1, source_text_2, alternate_texts)
for alt in result:
    print(alt)
