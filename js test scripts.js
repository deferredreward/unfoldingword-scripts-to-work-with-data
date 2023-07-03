
let appendedNote = '# Introduction to Ruth\n\n## Part 1: General Introduction\n\n### Outline of Ruth\n\n1. Naomi goes to Moab with her family (1:1–5)\n1. Ruth comes to Bethlehem with Naomi (1:6–22)\n1. Boaz helps Ruth as she gleans (2:1–23)\n1. Boaz and Ruth at the threshing floor (3:1–18)\n1. Ruth becomes the wife of Boaz (4:1–16)\n1. Obed born to Ruth and Boaz; the genealogy of David (4:13–22)\n\n### What is the book of Ruth about?\n\nThis book is about a non-Israelite woman named Ruth. It tells how she came to join the people of Yahweh. The book also explains how Ruth became an ancestor of King David.\n\n### How should the title of this book be translated?\n\nThis book traditionally has the title **Ruth** because she is the main person in it. If the church prefers, you could use a fuller title such as **The Book About Ruth**. (See: [[rc://*/ta/man/translate/translate-names]])\n\n### When did the events in the book of Ruth occur?\n\nThe story of Ruth is set during the time when there were judges in Israel. This was after the people of Israel had entered into the land of Canaan, but before they had a king. The judges were men and women whom God chose to help the Israelites defeat their enemies. These leaders usually continued to help the people by deciding disputes among them. They also helped the people make important decisions. Many of these leaders served all the people of Israel, but some of them may have served only certain tribes.\n\n## Part 2: Important Religious and Cultural Concepts\n\n### Why does death (Gen 50:22-26)\n\n### Special formatting\n\nThe book of Genesis sometimes uses poetic language to emphasize what is being said. Many translations use a special format to identify these passages as poetry by indenting each clause on a new line. Many other translations do not do this, but rather use regular paragraph formatting everywhere, including for poetry. It may be helpful to look at a translation in the national language of your country that uses poetry formatting, to help you decide whether or not you want to do something similar in your translation. Some translations put some of the following passages in poetry format since these verses have certain features of poetry such as parallelisms and metaphors: Genesis 1:27; 2:23; 3:14-16, 17b-19; 4:23-24; 8:22; 9:6, 25-27; 12:2-3; 14:19-20; 15:1; 16:11-12; 24:60; 25:23; 27:27-29, 39-40; 48:15-16, 20; 49:1-27. You may not want to put all these passages in poetry format since some of them have paralleli';



let lastChapter;
appendedNote = appendedNote.replace(/((?<=^|;|\s)\d+:\d+\w*)|(\b\d+\w*\b(?=,|$))/g, (match) => {
    if (match.includes(':')) {
        lastChapter = match.split(':')[0];
        return match;
    } else {
        return `${lastChapter}:${match}`;
    }
});

console.log(appendedNote);
