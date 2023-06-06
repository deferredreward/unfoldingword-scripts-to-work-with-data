const path = require('path');
const fse = require('fs-extra');
const { Proskomma } = require('proskomma');
const pk = new Proskomma();
let content = fse.readFileSync(path.resolve('C:\\Users\\benja\\Downloads\\ult\\', './06-JOS.usfm')).toString();

const queryPk = async function (pk, query) {
    const result = await pk.gqlQuery(query);
    const verses = result.data.documents[0].cvIndex.verses;

    verses.forEach((verseData) => {
        if (verseData.verse.length > 0) {
            const verseRange = verseData.verse[0].verseRange;
            const text = verseData.verse[0].text;
            console.log(verseRange);
            console.log(text);
        }
    });

    // console.log(JSON.stringify(result.data.documents[0].cvIndex.verses, null, 2));
    // const verses = result.data.documents[0].cvIndex.verses;

    // verses.forEach((verse) => {
    //     if (verse.length > 0) {
    //         console.log(JSON.stringify(verse[0].verseRange, null, 2));
    //     }
    // });
}

const mutation = `mutation { addDocument(` +
    `selectors: [{key: "lang", value: "eng"}, {key: "abbr", value: "ust"}], ` +
    `contentType: "usfm", ` +
    `content: """${content}""") }`;

queryPk(pk, mutation);

const dataQuery = `{
    documents {
       cvIndex(chapter:1) {
          verses {
             verse {
                verseRange
                text
             }
          }
       }
    }
 }`;
try {
    queryPk(pk, dataQuery);
} catch (error) {
    // Ignore the error
    console.error('An error occurred:', error);
}