const bookDictionary = {
    'Genesis': 'GEN',
    'Exodus': 'EXO',
    'Leviticus': 'LEV',
    'Numbers': 'NUM',
    'Deuteronomy': 'DEU',
    'Joshua': 'JOS',
    'Judges': 'JDG',
    'Ruth': 'RUT',
    '1 Samuel': '1SA',
    '2 Samuel': '2SA',
    '1 Kings': '1KI',
    '2 Kings': '2KI',
    '1 Chronicles': '1CH',
    '2 Chronicles': '2CH',
    'Ezra': 'EZR',
    'Nehemiah': 'NEH',
    'Esther': 'EST',
    'Job': 'JOB',
    'Psalms': 'PSA',
    'Psalm': 'PSA',
    'Proverbs': 'PRO',
    'Ecclesiastes': 'ECC',
    'Song of Songs': 'SNG',
    'Isaiah': 'ISA',
    'Jeremiah': 'JER',
    'Lamentations': 'LAM',
    'Ezekiel': 'EZK',
    'Daniel': 'DAN',
    'Hosea': 'HOS',
    'Joël': 'JOL',
    'Amos': 'AMO',
    'Obadiah': 'OBA',
    'Jonah': 'JON',
    'Micah': 'MIC',
    'Nahum': 'NAM',
    'Habakkuk': 'HAB',
    'Zephaniah': 'ZEP',
    'Haggai': 'HAG',
    'Zechariah': 'ZEC',
    'Malachi': 'MAL',
    'Matthew': 'MAT',
    'Mark': 'MRK',
    'Luke': 'LUK',
    'John': 'JHN',
    'Acts': 'ACT',
    'Romans': 'ROM',
    '1 Corinthians': '1CO',
    '2 Corinthians': '2CO',
    'Galatians': 'GAL',
    'Ephesians': 'EPH',
    'Philippians': 'PHP',
    'Colossians': 'COL',
    '1 Thessalonians': '1TH',
    '2 Thessalonians': '2TH',
    '1 Timothy': '1TI',
    '2 Timothy': '2TI',
    'Titus': 'TIT',
    'Philemon': 'PHM',
    'Hebrews': 'HEB',
    'James': 'JAS',
    '1 Peter': '1PE',
    '2 Peter': '2PE',
    '1 John': '1JN',
    '2 John': '2JN',
    '3 John': '3JN',
    'Jude': 'JUD',
    'Revelation': 'REV'
};

let BPready = ['GEN', 'EXO', 'RUT', 'EZR', 'EST', 'NEH', 'OBA', 'JON', 'MAT', 'MRK', 'LUK', 'JHN', 'ACT', 'ROM', '1CO', '2CO', 'GAL', 'EPH', 'PHP', 'COL', '1TH', '2TH', '1TI', '2TI', 'TIT', 'PHM', 'HEB', 'JAS', '1PE', '2PE', '1JN', '2JN', '3JN', 'JUD', 'REV'];

BPready = ['RUT'];

const fs = require('fs');
const fse = require('fs-extra');
const path = require('path');
const { create } = require('xmlbuilder2');
const { Proskomma } = require('proskomma');
const { getParsedUSFM, getTargetQuoteFromSourceQuote } = require("uw-quote-helpers");
let id;


// Paths for sourceBook and targetBook files
const sourceBookPaths = {
    ot: 'C:\\Users\\benja\\Documents\\uwgit\\hbo_uhb',
    nt: 'C:\\Users\\benja\\Documents\\uwgit\\el-x-koine_ugnt'
};

// paths for other files
const targetBookPath = 'C:\\Users\\benja\\Documents\\uwgit\\en_ult';
const notesStringPath = 'C:\\Users\\benja\\Documents\\uwgit\\en_tn';

// const files = fs.readdirSync(targetBookPath);

// Filter for usfm files and get book names
const books = fs.readdirSync(targetBookPath)
    .filter(file => path.extname(file) === '.usfm' && file !== 'A0-FRT.usfm')
    .map(file => path.basename(file, '.usfm'));

// need an 'old reference' so we don't have to keep querying the new one...
let oldRef = '0:0';

// Start of the XML document
const normal = { version: '1.0', encoding: 'utf-8' }//, noDoubleEncoding: true, noValidation: true}
let doc = create(normal)
    .ele('CommentList')
    .ele('Comment', {
        Thread: 'LicenseInfo',
        User: 'Benjamin Wright',
        VerseRef: 'GEN 1:0',
        Language: 'en-US',
        Date: getTimestamp(),
    })
    .ele('HideInTextWindow').txt('true').up()
    .ele('Contents').txt('unfoldingWord Translation Notes released under CC BY SA 4.0').up()
    .up();

function getTimestamp() {
    // Create a new date object
    let date = new Date();

    // Get the timezone offset in minutes
    let offset = date.getTimezoneOffset();

    // Convert the offset from minutes to milliseconds
    offset *= 60000;

    // Subtract the offset from the current date to get the date in local time
    date = new Date(date.getTime() - offset);

    // Get the current time in milliseconds
    let milliseconds = date.getMilliseconds();

    // Convert the milliseconds to microseconds by appending three zeros
    let microseconds = milliseconds * 1000;

    // Format the microseconds to match the required format
    let microsecondString = String(microseconds).padStart(6, '0');

    // Get the timestamp string without milliseconds
    let timestampWithoutMilliseconds = date.toISOString().split('.')[0];

    // Get the timezone offset in hours and minutes
    let timezoneOffset = -date.getTimezoneOffset() / 60;
    let timezoneOffsetString = timezoneOffset >= 0 ? '+' + timezoneOffset.toFixed(2) : '-' + Math.abs(timezoneOffset).toFixed(2);
    timezoneOffsetString = timezoneOffsetString.replace('.', ':');

    // Combine all parts to create the final timestamp string
    let timestamp = timestampWithoutMilliseconds + '.' + microsecondString + timezoneOffsetString;

    return timestamp;
}

function tsvMap(tsvString, rowsMap = (row) => row) {
    let columns;
    const tsvArray = tsvString.split('\n').map((line, index) => {
        const rowArray = line.split(/\t/);
        if (index === 0) {
            columns = rowArray;
            return;
        }
        const rowObject = rowArray.reduce((rowObject, value, index) => {
            rowObject[columns[index]] = value;
            return rowObject;
        }, {});
        return rowsMap(rowObject);
    }).filter(row => row);  // Filter out any undefined values (such as the first row)

    return { array: tsvArray, columns };
}

function findSourceBook(book) {
    // Extract the book number from the book string
    const bookNumber = parseInt(book.split('-')[0]);

    // Determine the correct path based on the book number
    let sourceBookPath;
    if (bookNumber >= 1 && bookNumber <= 39) {
        sourceBookPath = sourceBookPaths.ot;
    } else if (bookNumber >= 41 && bookNumber <= 67) {
        sourceBookPath = sourceBookPaths.nt;
    } else {
        throw new Error(`Invalid book: ${book}`);
    }
    console.log(path.resolve(sourceBookPath, `./${book}.usfm`));
    return getParsedUSFM(fse.readFileSync(path.resolve(sourceBookPath, `./${book}.usfm`)).toString()).chapters;
}

// async function getChapter(ref, pk) {

//     const query = `{documents {cvIndex(chapter:${ref.split(':')[0]}) {verses {verse {verseRange text}}}}}`;
//     const result = await pk.gqlQuery(query);
//     if (result != undefined) {
//         let dictionary = {};

//         for (let verseInfo of result.data.documents[0].cvIndex.verses) {
//             if (verseInfo.verse.length > 0) {
//                 let verseRange = verseInfo.verse[0].verseRange;
//                 let text = verseInfo.verse[0].text.replace(/\n/g, ' ').replace(/[{}]/g, '');
//                 dictionary[verseRange] = text;

//             }
//         }
//         return dictionary;
//     }

// }

async function getBook(pk) {

    const query = `{    documents {
        cvIndexes {
          chapter
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
    if (result != undefined) {
        let output = {};
        let documents = result.data.documents;

        documents.forEach((document) => {
            let cvIndexes = document.cvIndexes;
            cvIndexes.forEach((cvIndex) => {
                let chapter = cvIndex.chapter;
                let verses = cvIndex.verses;
                verses.forEach((verse) => {
                    verse.verse.forEach((detail) => {
                        let verseRange = detail.verseRange;
                        let text = detail.text.replace(/\n/g, ' ');
                        output[`${chapter}:${verseRange}`] = text;
                    });
                });
            });
        });
        return output;
    }
}

const readFirstLine = require('read-first-line');

async function getFolderTitleDictionary(dirPath) {
    let dictionary = {};

    // Read all folders in the directory
    const folders = fs.readdirSync(dirPath, { withFileTypes: true })
        .filter(dirent => dirent.isDirectory())
        .map(dirent => dirent.name);

    // Loop through each folder and read the first line of the 'title.md' file
    for (let folder of folders) {
        const filePath = path.join(dirPath, folder, 'title.md');

        if (fs.existsSync(filePath)) {
            const firstLine = await readFirstLine(filePath);
            dictionary[folder] = firstLine;
        }
    }

    return dictionary;
}

function writeParatextNote(book, ref, id, glQuote, occurrence, note, wholeVerse) {
    // console.log(book, ref, id, glQuote, occurrence, note, wholeVerse);
    let startPosition, contextBefore, contextAfter;
    if (glQuote) {
        if (occurrence > 1) {
            let i = -1;
            while (occurrence-- && i++ < wholeVerse.length) {
                i = wholeVerse.indexOf(glQuote, i);
                if (i < 0) break;
            }
            startPosition = i;
        } else {
            startPosition = wholeVerse.indexOf(glQuote);
        }
        if (glQuote.includes('&')) {
            contextBefore = "Occurrences of: "
            contextAfter = ` ${wholeVerse}`;
        } else {
            contextBefore = wholeVerse.substring(0, startPosition).trimStart();
            contextAfter = wholeVerse.substring(startPosition + glQuote.length).trimEnd();
        }
    }

    let comment = doc.ele('Comment', {
        Thread: id, // As an example, I'm using id here. Replace it with the correct attribute.
        User: 'unfoldingWord',
        VerseRef: `${book} ${ref.replace('front', '1').replace('intro', '0')}`, // Assuming ref is the correct verse reference
        Language: 'en-US',
        Date: getTimestamp(),
    });

    if (glQuote != undefined && glQuote.trim() !== '') {
        comment = comment.ele('SelectedText').txt(glQuote).up();
    }
    if (startPosition != undefined && startPosition !== '') {
        comment = comment.ele('StartPosition').txt(startPosition).up();
    }
    if (contextBefore != undefined && contextBefore.trim() !== '') {
        comment = comment.ele('ContextBefore').txt(contextBefore).up();
    }
    if (contextAfter != undefined && contextAfter.trim() !== '') {
        comment = comment.ele('ContextAfter').txt(contextAfter).up();
    }
    if (wholeVerse != undefined && wholeVerse.trim() !== '') {
        comment = comment.ele('Verse').txt(wholeVerse).up();
    }
    comment = comment.ele('HideInTextWindow').txt('false').up();
    if (note != undefined && note.trim() !== '') {
        comment = comment.ele("Contents");
        let pieces = note.split(/(uniqueStartBoldTag|uniqueEndBoldTag|uniqueBreakTag)/);

        let isBold = false;
        for (let piece of pieces) {
            if (piece === 'uniqueStartBoldTag') {
                isBold = true;
            } else if (piece === 'uniqueEndBoldTag') {
                isBold = false;
            } else if (piece === 'uniqueBreakTag') {
                comment = comment.ele("br").up();
            } else if (isBold) {
                comment = comment.ele("bold").txt(piece).up();
            } else {
                comment = comment.txt(piece); // just add the piece as text
            }
        }
        comment = comment.up();
    }
}


async function main() {
    try { // Processing for each book
        const dictionary = await getFolderTitleDictionary('C:\\Users\\benja\\Documents\\uwgit\\en_ta\\translate');

        for (let book of books) {

            oldRef = '0:0';
            // Proskomma instance
            const pk = new Proskomma();
            const shortbook = book.slice(3);
            if (!BPready.includes(shortbook)) { continue; };
            const currentTargetBookString = fse.readFileSync(path.resolve(targetBookPath, `./${book}.usfm`)).toString();
            const currentTargetBook = getParsedUSFM(currentTargetBookString).chapters;

            const currentTNBook = fse.readFileSync(path.resolve(notesStringPath, `./tn_${shortbook}.tsv`)).toString();

            const currentSourceBook = findSourceBook(book);

            const mutation = `mutation { addDocument(` +
                `selectors: [{key: "lang", value: "eng"}, {key: "abbr", value: "ult"}], ` +
                `contentType: "usfm", ` +
                `content: """${currentTargetBookString}""") }`;
            let m = await pk.gqlQuery(mutation);
            console.time("getBookTime");
            let wholeBook = await getBook(pk);
            console.timeEnd("getBookTime");
            // Parse TSV data
            const { array: tsvData } = tsvMap(currentTNBook);

            let wholeChapter, wholeVerse;
            for (let i = 0; i < tsvData.length; i++) {
                const row = tsvData[i];
                if (row["Reference"] == '') { continue; }
                const ref = row["Reference"];
                // if (!ref.startsWith('3:')) continue;
                id = row["ID"];

                // tags aren't used in TNs
                const supportRef = row["SupportReference"];
                const quote = row["Quote"];
                const occurrence = row["Occurrence"];
                const note = row["Note\r"];
                let appendedNote;
                appendedNote = note;

                const params = {
                    quote,
                    ref,
                    sourceBook: currentSourceBook,
                    targetBook: currentTargetBook,
                    options: { occurrence, fromOrigLang: true },
                };
                let glQuote = '';
                if (quote && occurrence > 0) {
                    glQuote = getTargetQuoteFromSourceQuote(params);
                    if (oldRef != ref) {
                        let [chapter, verse] = ref.split(':', 2);
                        let regex = /\D/;
                        if (regex.test(verse)) {
                            // console.log(`problem ref ${ref}`);
                            verse = verse.split(/\D/, 2)[0];
                            appendedNote = `Note applies to: ${ref}. ${appendedNote}`;
                        }

                        wholeVerse = wholeBook[`${chapter}:${verse}`];
                        oldRef = ref;
                    }
                }

                appendedNote = appendedNote.replace(/\\n\\n/g, 'uniqueBreakTag');
                appendedNote = appendedNote.replace(/\\n/g, 'uniqueBreakTag');
                appendedNote = appendedNote.replace(/<br><br>/g, 'uniqueBreakTag');
                appendedNote = appendedNote.replace(/<br>/g, 'uniqueBreakTag');
                appendedNote = appendedNote.replace(/\*\*(.*?)\*\*/g, 'uniqueStartBoldTag$1uniqueEndBoldTag');

                // properly direct inline TA link
                const inlineTAlink = /\[{2}rc:\/\/\*\/ta\/man\/translate\/(.*?)\]{2}/g;
                appendedNote = appendedNote.replace(inlineTAlink, (match, supportRefKey) => {
                    const supportRefValue = dictionary[supportRefKey] || '';
                    const replacement = `${supportRefValue} at https://git.door43.org/unfoldingWord/en_ta/src/branch/master/translate/${supportRefKey}/01.md`;
                    return replacement;
                });
                // properly direct inline TW link
                appendedNote = appendedNote.replace(/\[{2}rc:\/\/\*\/tw\/dict\/bible\/(.*?)\]{2}/g, function (_, match) {
                    let afterSlashIndex = match.lastIndexOf("/") + 1;
                    let stringAfterSlash = match.substring(afterSlashIndex);
                    stringAfterSlash = stringAfterSlash.charAt(0).toUpperCase() + stringAfterSlash.slice(1);
                    return `${stringAfterSlash} at https://git.door43.org/unfoldingWord/en_tw/src/branch/master/bible/${match}.md`;
                });

                // process reference links
                // this tries to make all notes be chapter:verse even if they're in a list
                // let lastChapter;
                // appendedNote = appendedNote.replace(/(\d+:\d+\w*)|(\b\d+\w*\b)/g, (match) => {
                //     if (match.includes(':')) {
                //         lastChapter = match.split(':')[0];
                //         return match;
                //     } else {
                //         return `${lastChapter}:${match}`;
                //     }
                // });


                if (appendedNote.includes('./')) {
                    // console.log(appendedNote);
                    const oddLink1 = /\[(.*?)(\d{1,3}[^:]*?)\]\((.*?intro.*?)\.md\)/;
                    if (oddLink1.test(appendedNote)) {
                        appendedNote = appendedNote.replace(/\[(.*?)(\d{1,3}[^:]*?)\]\((.*?intro.*?)\.md\)/g, '$1$2');
                    }

                    // find unmarked links to other books
                    appendedNote = appendedNote.replace(/\[(\d{1,3}:\d{1,3}.*?)\]\(\.\.\/(\w{3})\/(\d{1,3})\/(\d{1,3})\.md\)/g, function (match, p1, p2, p3, p4) {
                        return `${p2.toUpperCase()} ${String(parseInt(p3, 10))}:${String(parseInt(p4, 10))}`;
                    });
                    // drop duplicate book names
                    for (let [key, value] of Object.entries(bookDictionary)) {
                        let regex = new RegExp(`${key} ${value}`, 'g');
                        appendedNote = appendedNote.replace(regex, value);
                    }

                    // find links to verses with chapters ([12:15](link.md))
                    appendedNote = appendedNote.replace(/\[(\d{1,3}:\d{1,3}.*?)\]\(.*?md\)/g, '$1');

                    // find links to other books
                    otherbookregex = /\[(.*?) (\d{1,3}:\d{1,3}.*?)\]\(.*?md\)/;
                    let soManyReferenceLinks = 0;
                    while (otherbookregex.test(appendedNote)) {
                        if (soManyReferenceLinks > 150) {
                            console.log(`problem or more than 150 references @ ${id, shortbook, ref}, moving on`);
                            break;
                        }
                        soManyReferenceLinks = soManyReferenceLinks + 1;
                        // console.log(appendedNote);
                        appendedNote = appendedNote.replace(otherbookregex, function (fullMatch, group1, group2) {
                            // Trim and check if group1 exists in the dictionary
                            let trimmedGroup1 = group1.trim();
                            if (trimmedGroup1 in bookDictionary) {
                                // if we're in the same book we don't need the book
                                if (bookDictionary[trimmedGroup1] == shortbook) {
                                    return group2;
                                }
                                // If it does, replace group1 with the dictionary value
                                return `${bookDictionary[trimmedGroup1]} ${group2}`; // testing
                            }
                            // If it doesn't, return the match unmodified
                            return fullMatch;
                        });
                    }

                    //find simple verse links
                    appendedNote = appendedNote.replace(/( verse )\[(\d{1,3})\]\(.*?md\)/g, 'v$2');
                    appendedNote = appendedNote.replace(/( v )\[(\d{1,3})\]\(.*?md\)/g, 'v$2');
                    appendedNote = appendedNote.replace(/( v. )\[(\d{1,3})\]\(.*?md\)/g, 'v$2');
                    appendedNote = appendedNote.replace(/( verses )\[(\d{1,3}.*?)\]\(.*?md\)/g, 'v$2');
                    appendedNote = appendedNote.replace(/( vv. )\[(\d{1,3}.*?)\]\(.*?md\)/g, 'v$2');
                }


                if (supportRef != '') {
                    // Parse the supportRef and get the corresponding value from the dictionary
                    const supportRefKey = supportRef.split('/').pop();
                    const supportRefValue = dictionary[supportRefKey] || '';

                    // Append to the note
                    appendedNote = `${appendedNote} (See “${supportRefValue}” at https://git.door43.org/unfoldingWord/en_ta/src/branch/master/translate/${supportRefKey}/01.md)`;
                }

                glQuote = glQuote.replace(/[{}]/g, '');
                writeParatextNote(shortbook, ref, id, glQuote, occurrence, appendedNote, wholeVerse);
            }
        }

        // Write XML to file
        fs.writeFileSync('C:\\Users\\benja\\Downloads\\Notes_Benjamin Wright.xml', doc.end({ prettyPrint: true }));
    }
    catch (error) {
        fs.writeFileSync('C:\\Users\\benja\\Downloads\\Notes_Benjamin Wright.xml', doc.end({ prettyPrint: true }));
        console.log(id);//, supportRef, quote, occurrence, note, book, ref);
        console.error(error);
        // Handle the error here if needed
    }
};
main().catch(error => console.error(error));
