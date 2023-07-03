const path = require('path');
const fse = require('fs-extra');
const { Proskomma } = require('proskomma');
const pk = new Proskomma();
let content = fse.readFileSync(path.resolve('C:\\Users\\benja\\Documents\\uwgit\\en_ult\\', './32-JON.usfm')).toString();

const queryPk = async function (pk, query) {
    const result = await pk.gqlQuery(query);
    // const cvArray = result.data.documents[0].cv;
// const texts = cvArray.map(item => item.text.replace(/\n/g, ' ').replace(/[{}]/g, ''));
    console.log(JSON.stringify(result, null, 2));
//     let dictionary = {};

//     for (let verseInfo of result.data.documents[0].cvIndex.verses) {
//         if (verseInfo.verse.length > 0) {
//             let verseRange = verseInfo.verse[0].verseRange;
//             let text = verseInfo.verse[0].text.replace(/\n/g, ' ').replace(/[{}]/g, '');
//             dictionary[verseRange] = text;
//         }
//     }
// // console.log(dictionary);
// console.log(dictionary["1"]);

    // console.log(result.data.documents[0].cv[0].text.replace(/\n/g, ' ').replace(/[{}]/g, ''));
    // console.log(texts);

    //ingest a whole book:
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

console.log(output);




};
const mutation = `mutation { addDocument(` +
    `selectors: [{key: "lang", value: "eng"}, {key: "abbr", value: "ust"}], ` +
    `contentType: "usfm", ` +
    `content: """${content}""") }`;

    pk.gqlQuery(mutation);
const ref = '1:5-6'
const myQuery = `{    documents {
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
}`


try {
    queryPk(pk, myQuery);
} catch (error) {
    // Ignore the error
    console.error('An error occurred:', error);
}


//    // Create a write stream to the log file
//    const logStream = fs.createWriteStream(logFilePath, { flags: 'a' });
    
//    // Override the console.log() method
//    console.log = function (message) {
//      logStream.write(`${message}\n`);
//    };
   
//    // Usage example
//    console.log(JSON.stringify(result, null, 2));
//    // Remember to close the write stream when done
//    logStream.end();