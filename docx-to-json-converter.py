import docx
import json

def docx_to_json(input_file, output_file):
    doc = docx.Document(input_file)
    data = []
    current_entry = {}
    fields = [
        "type_of_translation_issue", "SupportReference", "BibleRef", 
        "BibleVerse", "VerseSnippet", "translationNote", "alternateTranslations"
    ]
    field_index = 0

    for paragraph in doc.paragraphs:
        if paragraph.text.strip() == "":
            if current_entry:
                data.append(current_entry)
                current_entry = {}
                field_index = 0
        else:
            if field_index < len(fields):
                current_entry[fields[field_index]] = paragraph.text.strip()
                field_index += 1

    if current_entry:
        data.append(current_entry)

    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    print(f"Conversion complete. JSON file saved as {output_file}")

# Usage
input_file = "tnSamples.docx"
output_file = "tnSamples.json"
docx_to_json(input_file, output_file)
