const { create } = require('xmlbuilder2');

let note = 'something that includes <bold>text</bold> in it';

let doc = create({ version: '1.0', encoding: 'UTF-8' })
  .ele('Root')
    .ele('Contents').raw(note).up()
  .end({ prettyPrint: true });

console.log(doc);
