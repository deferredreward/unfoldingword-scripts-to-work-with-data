const path = require('path');
const fse = require('fs-extra');
const { Proskomma } = require('proskomma');
const pk = new Proskomma();

const ust_file = path.resolve('C:\\Users\\benja\\Downloads\\ust\\', './01-GEN.usfm');
const ult_file = path.resolve('C:\\Users\\benja\\Downloads\\ult\\', './01-GEN.usfm');
const tsv_file = path.resolve('C:\\Users\\benja\\Documents\\uwgit\\en_tn\\tn_GEN.tsv');
const output_file = path.resolve('C:\\Users\\benja\\Downloads\\tn_GEN.tsv');

const generate_all_alternatives = (text) => {
  const components = text.split();

  // For each component, split by '/' to create a list of alternatives
  const alternatives = components.map(comp => comp.split('/'));

  // Generate all possible combinations of alternatives
  const sentences = alternatives.reduce((a, b) => a.concat(b), []);
  return sentences;
};

const choose_alternatives = (source1, source2, alternatives) => {
  source1 = source1.replace("{", "").replace("}", "");
  source2 = source2.replace("{", "").replace("}", "");

  const all_alternatives = [];
  for (const alt of alternatives) {
    const alt_sentences = generate_all_alternatives(alt);

    // Valid alternatives are those that are not in the source texts
    const valid_alt_sentences = alt_sentences.filter(sentence => sentence !== source1 && sentence !== source2);

    all_alternatives.push(valid_alt_sentences);
  }

  // Choose a random alternative from each list of valid alternatives
  const chosen_alternatives = all_alternatives.map(alts => alts[Math.floor(Math.random() * alts.length)]);

  return chosen_alternatives;
};

const process_alternates = (line) => {
  // Get the reference and note from the line
  const [reference, note] = line.split('\t', 1);

  // Get the alternate translations from the note
  const alternate_texts = note && note.match(/"(.*?)"/g);

  // If there are no alternate translations, return the original line
  if (!alternate_texts) {
    return line;
  }

  // Process the alternate translations
  const chosen_alternatives = choose_alternatives(source_text_1, source_text_2, alternate_texts);

  // Create a new line with the alternate translations
  const new_line = reference + '\t' + note.replace(alternate_texts[0], 'Alternate translation: ' + chosen_alternatives.join(' or '));

  return new_line;
};

const main = async () => {
  // Open the source files
  const ust_content = await fse.readFile(ust_file, 'utf8');
  const ult_content = await fse.readFile(ult_file, 'utf8');

  // Create the output file
  await fse.writeFile(output_file, '', 'utf8');

  // Process each line in the tsv file
  for await (const line of fse.readFileSync(tsv_file, 'utf8').split('\n')) {
    // Process the alternate translations
    new_line = process_alternates(line);

    // Write the new line to the output file
    await fse.appendFile(output_file, new_line + '\n', 'utf8');
  }
};

main();
