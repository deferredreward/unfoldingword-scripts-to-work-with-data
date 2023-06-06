let str = "“After those things/events happened,” or “After that,”";

let regexRemove2 = /^“.*?”\.? ?([A-Z]|\n)(.*)/;
str = str.replace(regexRemove2, '$1$2');

console.log("new string: " + str);