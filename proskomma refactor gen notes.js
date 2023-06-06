const fs = require('fs');
const csv = require('csv-parser');
const tsvWriter = require('fast-csv');
const path = require('path');
const fse = require('fs-extra');
const { Proskomma } = require('proskomma');

const pk1 = new Proskomma();
const pk2 = new Proskomma();

let content1 = fse.readFileSync(path.resolve('C:\\Users\\benja\\Downloads\\ult\\', './01-GEN.usfm')).toString();
let content2 = fse.readFileSync(path.resolve('C:\\Users\\benja\\Downloads\\ust\\', './01-GEN.usfm')).toString();

async function main() {
    const mutation1 = `mutation { addDocument(` +
        `selectors: [{key: "lang", value: "eng"}, {key: "abbr", value: "ult"}], ` +
        `contentType: "usfm", ` +
        `content: """${content1}""") }`;

    const mutation2 = `mutation { addDocument(` +
        `selectors: [{key: "lang", value: "eng"}, {key: "abbr", value: "ust"}], ` +
        `contentType: "usfm", ` +
        `content: """${content2}""") }`;

    // Load all verses
    await pk1.gqlQuery(mutation1);
    const verseDict1 = await loadAllVerses(pk1, "GEN");
    await pk2.gqlQuery(mutation2);
    const verseDict2 = await loadAllVerses(pk2, "GEN");
    // console.log(verseDict2)


    function generate_all_alternatives(text) {
        let components = text.split(' ');

        // For each component, split by '/' to create a list of alternatives
        let alternatives = components.map(comp => comp.split('/'));

        // Initialize the array of combinations with a single, empty combination
        let allCombinations = [''];

        // For each set of alternatives...
        for (let i = 0; i < alternatives.length; i++) {
            let temp = [];
            // For each existing combination...
            for (let j = 0; j < allCombinations.length; j++) {
                // For each alternative in the current set of alternatives...
                for (let k = 0; k < alternatives[i].length; k++) {
                    // Add the current alternative to the current combination
                    temp.push(allCombinations[j] + (allCombinations[j] ? ' ' : '') + alternatives[i][k]);
                }
            }
            allCombinations = temp;
        }
        // console.log(allCombinations); // this works!
        return allCombinations;
    }

    async function generateAlternatives(note, source1, source2) {
        // Extract alternatives from the note
        const regex = /^“([^”]+?)”( ?or ?(“([^”]+?)”))?( ?or ?(“([^”]+?)”))?( ?or ?(“([^”]+?)”))?( ?or ?(“([^”]+?)”))?( ?or ?(“([^”]+?)”))?( ?or ?(“([^”]+?)”))?/g;
        let alternates;
        let alternatives = [];
        while ((alternates = regex.exec(note)) !== null) {
            for (let i = 0; i < alternates.length; i++) {
                const item = alternates[i];

                if (item === undefined || item.includes("“") || item.includes("”") || item.includes("‘") || item.includes("’")) {
                    continue; // Skip undefined or items with curly quotes
                }
                alternatives.push(item);
            }
        }

        // Generate all possible combinations of alternatives
        let allCombinations = [];
        alternatives.forEach((alt) => {
            let combinations = generate_all_alternatives(alt);
            allCombinations.push(combinations);
        });

        // Filter the combinations that already exist in the sources
        // And find the most different alternative for each sublist
        let validAlternatives = allCombinations.map((altList) => {
            let validAltList = altList.filter((alt) => {
                return source1.indexOf(alt) === -1 && source2.indexOf(alt.replace(/[.,;:!?]+$/, "")) === -1;
            });

            // Find the most different alternative
            let mostDifferentAlt = findMostDifferent(source1, source2, validAltList);
            
            return mostDifferentAlt;
        });

        return validAlternatives;
    }

    function levenshteinDistance(a, b) {
        const matrix = [];

        // Increment along the first column of each row
        let i;
        for (i = 0; i <= b.length; i++) {
            matrix[i] = [i];
        }

        // Increment each column in the first row
        let j;
        for (j = 0; j <= a.length; j++) {
            matrix[0][j] = j;
        }

        // Fill in the rest of the matrix
        for (i = 1; i <= b.length; i++) {
            for (j = 1; j <= a.length; j++) {
                if (b.charAt(i - 1) === a.charAt(j - 1)) {
                    matrix[i][j] = matrix[i - 1][j - 1];
                } else {
                    matrix[i][j] = Math.min(matrix[i - 1][j - 1] + 1, // substitution
                        Math.min(matrix[i][j - 1] + 1, // insertion
                            matrix[i - 1][j] + 1)); // deletion
                }
            }
        }

        return matrix[b.length][a.length];
    }

    function findMostDifferent(str1, str2, alternates) {
        let mostDifferent = '';
        let maxDistance = 0;

        alternates.forEach(alt => {
            const distance = levenshteinDistance(str1, alt) + levenshteinDistance(str2, alt);
            if (distance > maxDistance) {
                mostDifferent = alt;
                maxDistance = distance;
            }
        });

        return mostDifferent;
    }



    async function loadAllVerses(pk, book) {
        let verseDict = {};
        for (let c = 1; c <= 50; c++) {
            const query = `
            {
                documents {
                    cvIndex(chapter:${c}) {
                        verses {
                            verse {
                                verseRange
                                text
                            }
                        }
                    }
                }
            }`;
            const result = await pk.gqlQuery(query);
            if (result && result.data && result.data.documents[0]) {
                result.data.documents[0].cvIndex.verses.forEach((verseData) => {
                    const chapterNumber = c;
                    if (verseData.verse.length > 0) {
                        const verseNumber = verseData.verse[0].verseRange;
                        let cv = chapterNumber + ':' + verseNumber;
                        verseDict[cv] = verseData.verse[0].text.replace(/[{}]/g, '');
                    }
                });
            }
        }
        return verseDict;
    }



    const results = [];
    fs.createReadStream('C:\\Users\\benja\\Documents\\uwgit\\en_tn\\tn_GEN.tsv')  // Replace with actual path
        .pipe(csv({ separator: '\t' }))
        .on('data', async (row) => {
            const reference = row['Reference'];
            if (reference.startsWith('front') || reference.endsWith(':intro')) {
                results.push(row);
                return;
            }

            let source1 = verseDict1[reference];
            let source2 = verseDict2[reference];


            let validAlternatives = await generateAlternatives(row['Note'], source1, source2);

            // Ignore any blank items in validAlternatives
            validAlternatives = validAlternatives.filter(alt => alt.trim() !== "");

            // Replace anything in the first group of the regex in every note without touching what's in the 2nd group
            let regexRemove = /^“.*?”\.? ?([A-Z]|\n|\r|$)(.*)/;
            row['Note'] = row['Note'].replace(regexRemove, '$1$2' || '');

            if (validAlternatives.length > 0) {

                // Add each alt inside curly quotes, with ' or ' between any alts but not at the end
                row['Note'] += ' Alternate translation: ' + validAlternatives.map(alt => `“${alt}”`).join(' or ');
                results.push(row);
            }
            else if (row['Note'].length > 0) results.push(row); // these should be notes that just didn't have an AT

        })
        .on('end', () => {
            const ws = fs.createWriteStream('C:\\Users\\benja\\Downloads\\tn_GEN.tsv');

            tsvWriter
                .write(results, { headers: ['Reference', 'ID', 'Tags', 'SupportReference', 'Quote', 'Occurrence', 'Note'], delimiter: '\t' })
                .pipe(ws)
                .on("finish", function () {
                    console.log("CSV file written.");
                });

        });
}

main().catch(error => console.error(error));
