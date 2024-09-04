import os
import json

input_file = "C:\\Users\\benja\\Documents\\GitHub\\unfoldingword-scripts-to-work-with-data\\learn openai\\Figure-of-speech-translation-notes.txt"
output_file = "figure_of_speech_finetuning.json"

data = []

with open(input_file, "r", encoding="utf-8") as f:
    lines = f.readlines()

i = 0
translation_issue = ''
while i+5 < len(lines):
    if ":" in lines[i]:
        translation_issue = "figs-" + lines[i-2].strip().lower()
        text_with_issue = lines[i + 1].strip()
        translation_note = lines[i + 2].strip()
        print(translation_issue)
        text_with_issue2 = lines[i + 5].strip()
        translation_note2 = lines[i + 6].strip()
        i += 7


        fine_tuning = '{"messages": [{"role": "system", "content": "You are a Bible translation consultant writing translation issues in the Bible. These translation notes will include chapter and verse, an explanation of the translation issue, an alternate way to translate the idea without using the figure of speech, and the words from the Bible translation that need to be replaced to include the alternate translation. In order to accomplish this goal, I want you to provide me with the precise data I request. You should not provide explanations and interpretation unless you are specifically asked to do so. I am providing you with an example of a text of scripture along with a note explaining it. Before the note in the response is a code for the figure of speech characterized by figs-[type of figure]. rquestion is a rhetorical question. Use this to help you classify issues in future texts you are given."}, {"role": "user", "content": "'+ text_with_issue + '"}, {"role": "assistant", "content": "' + translation_issue + '\t' + translation_note + '"}]}\n{"messages": [{"role": "system", "content": "You are a Bible translation consultant writing translation issues in the Bible. These translation notes will include chapter and verse, an explanation of the translation issue, an alternate way to translate the idea without using the figure of speech, and the words from the Bible translation that need to be replaced to include the alternate translation. In order to accomplish this goal, I want you to provide me with the precise data I request. You should not provide explanations and interpretation unless you are specifically asked to do so. I am providing you with an example of a text of scripture along with a note explaining it. Before the note in the response is a code for the figure of speech characterized by figs-[type of figure]. rquestion is a rhetorical question. Use this to help you classify issues in future texts you are given."}, {"role": "user", "content": "'+ text_with_issue2 + '"}, {"role": "assistant", "content": "' + translation_issue + '\t' + translation_note2 + '"}]}\n'

        data.append(fine_tuning)
    else:
        i += 1

with open(output_file, "w", encoding="utf-8") as f:
    for a in data:
        f.write(str(a))

print(f"JSON file '{output_file}' created with {len(data)} examples.")