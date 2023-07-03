const fs = require('fs');
const fse = require('fs-extra');
const path = require('path');
const { create } = require('xmlbuilder2');
const { Proskomma } = require('proskomma');
const { getParsedUSFM, getTargetQuoteFromSourceQuote } = require("uw-quote-helpers");

// Proskomma instance
const pk = new Proskomma();

// Paths for sourceBook and targetBook files, to be completed
const sourceBookPaths = {
    ot: 'C:\\Users\\benja\\Documents\\uwgit\\hbo_uhb',
    nt: 'C:\\Users\\benja\\Documents\\uwgit\\el-x-koine_ugnt'
};

const targetBookPath = 'C:\\Users\\benja\\Documents\\uwgit\\en_ult';
const notesStringPath = 'C:\\Users\\benja\\Documents\\uwgit\\en_tn';

function getBooksFromPath(path) {
    const files = fs.readdirSync(path);

    // Filter for tsv files and get book names
    const books = files
        .filter(file => path.extname(file) === '.usfm' && file !== 'A0-FRT.usfm')
        .map(file => path.basename(file, '.usfm'));
        
    return books;
}

function getSourceBookPath(bookNumber) {
    let sourceBookPath;

    if (bookNumber >= 1 && bookNumber <= 39) {
        sourceBookPath = sourceBookPaths.ot;
    } else if (bookNumber >= 40 && bookNumber <= 66) {
        sourceBookPath = sourceBookPaths.nt;
    } else {
        throw new Error(`Invalid book number: ${bookNumber}`);
    }

    return sourceBookPath;
}

async function processRow(row, currentSourceBook, currentTargetBook) {
    const quote = row["Quote"];
    const ref = row["Reference"];
    const occurrence = row["Occurrence"];
    const id = row["ID"];
    const supportRef = row["SupportReference"]
    const params = {
        quote,
        ref,
        sourceBook: currentSourceBook,
        targetBook: currentTargetBook,
        options: { occurrence, fromOrigLang: true },
    };

    let glQuote;
    if (quote && occurrence > 0) {
        glQuote = getTargetQuoteFromSourceQuote(params);
        const query = `{documents { cv ( chapterVerses:"${ref}" ) { text }}}`
        const result = await pk.gqlQuery(query);
        console.log(JSON.stringify(result, null, 2));
        if (result != undefined) {
            console.log(result.data.documents[0].cv[0].text.replace(/\n/g, ' ').replace(/[{}]/g, ''));
        }
        else { console.log('grr'); }
    }
    else {
        console.log(ref, params.options, row['Note']);
    }
}

async function processBook(book) {
    const currentTargetBookString = fse.readFileSync(path.resolve(targetBookPath, `./${book}.usfm`)).toString();
    const currentTargetBook = getParsedUSFM(currentTargetBookString).chapters;

    const shortbook = book.slice(3);
    const currentTNBook = fse.readFileSync(path.resolve(notesStringPath, `./tn_${shortbook}.tsv`)).toString();

    // Extract the book number from the book string
    const bookNumber = parseInt(book.split('-')[0]);

    const sourceBookPath = getSourceBookPath(bookNumber);

    const currentSourceBook = getParsedUSFM(fse.readFileSync(path.resolve(sourceBookPath, `./${book}.usfm`)).toString()).chapters;

    const mutation = `mutation { addDocument(` +
        `selectors: [{key: "lang", value: "eng"}, {key: "abbr", value: "ult"}], ` +
        `contentType: "usfm", ` +
        `content: """${currentTargetBookString}""") }`;
    let m = await pk.gqlQuery(mutation);
    console.log(JSON.stringify(m, null, 2));

    // Parse TSV data
    const { array: tsvData } = tsvMap(currentTNBook);

    for (let row of tsvData) {
        await processRow(row, currentSourceBook, currentTargetBook);
    }
}

async function main() {
    const books = getBooksFromPath(targetBookPath);

    for (let book of books) {
        if (book == "01-GEN") { continue };
        await processBook(book);
    }

    // Write XML to file
    fs.writeFileSync('C:\\Users\\benja\\Downloads\\Notes_Benjamin Wright.xml', doc.end({ prettyPrint: true }));
};

main().catch(error => console.error(error));
